"""Basic code sandbox: static blocklist + isolated subprocess + time/memory limits.
Good for demos and local use. For public deployment, run inside Docker/gVisor or use Judge0."""
import json, os, re, subprocess, sys, tempfile

BLOCKED = re.compile(
    r"\b(import\s+(os|sys|subprocess|socket|shutil|pathlib|ctypes|requests|urllib|http|multiprocessing|threading|signal)\b"
    r"|from\s+(os|sys|subprocess|socket|shutil|pathlib|ctypes|requests|urllib|http)\b"
    r"|__import__|open\s*\(|eval\s*\(|exec\s*\(|compile\s*\(|globals\s*\(|locals\s*\(|getattr\s*\(|setattr\s*\(|input\s*\()")

RUNNER = '''
import json, sys
{code}
_tests = json.loads(sys.stdin.read())
_res = []
for _t in _tests:
    try:
        _out = solution(*_t["input"])
        _res.append({{"ok": _out == _t["expected"], "got": repr(_out)[:200]}})
    except Exception as e:
        _res.append({{"ok": False, "got": (type(e).__name__ + ": " + str(e))[:200]}})
print("@@RESULT@@" + json.dumps(_res))
'''


def _limits():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
        resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    except Exception:
        pass  # not available on Windows


def run_tests(code, tests):
    if BLOCKED.search(code):
        return {"error": "That import or function is not allowed in the sandbox", "results": []}
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(RUNNER.format(code=code)); path = tf.name
    try:
        kw = {"preexec_fn": _limits} if os.name == "posix" else {}
        r = subprocess.run([sys.executable, "-I", path], input=json.dumps(tests), capture_output=True, text=True, timeout=5, **kw)
    except subprocess.TimeoutExpired:
        return {"error": "Time limit exceeded (5s)", "results": []}
    finally:
        os.unlink(path)
    line = next((l for l in r.stdout.splitlines() if l.startswith("@@RESULT@@")), None)
    if not line:
        if r.returncode < 0:
            return {"error": "Time or memory limit exceeded", "results": []}
        lines = r.stderr.strip().splitlines()
        return {"error": lines[-1] if lines else "Your code did not run", "results": []}
    return {"error": None, "results": json.loads(line[len("@@RESULT@@"):])}
