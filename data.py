"""Static content: domains, learning modules, jobs, challenges, interview questions."""

def M(title, hours, lessons, resource):
    return {"title": title, "hours": hours, "lessons": lessons.split(";"), "resource": resource}

DOMAINS = {
    "AI & ML": {
        "roles": ["ML Engineer", "NLP Engineer", "Computer Vision Engineer", "AI Researcher"],
        "skills": ["Python", "NumPy", "Pandas", "Scikit-learn", "TensorFlow", "PyTorch", "Statistics", "Deep Learning", "NLP", "SQL"],
        "modules": [
            M("Python & Math Foundations", 20, "Python basics;NumPy arrays;Linear algebra;Probability", "Kaggle Learn: Python"),
            M("Machine Learning Algorithms", 30, "Regression;Classification;Trees & ensembles;Model evaluation", "Andrew Ng: ML Specialization"),
            M("Deep Learning with PyTorch", 30, "Neural nets;CNNs;RNNs & transformers;Training tricks", "fast.ai Practical Deep Learning"),
            M("NLP or Computer Vision Project", 25, "Text preprocessing;Embeddings;Fine-tuning;Build a demo", "Hugging Face Course"),
            M("MLOps & Deployment", 20, "Model serving with Flask;Docker;Monitoring;CI for ML", "Made With ML"),
        ]},
    "Web Development": {
        "roles": ["Frontend Developer", "Backend Developer", "Full Stack Developer"],
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Python", "Flask", "SQL", "REST", "Git"],
        "modules": [
            M("HTML, CSS & Responsive Design", 20, "Semantic HTML;Flexbox & Grid;Responsive layouts;Accessibility", "MDN Learn Web Development"),
            M("JavaScript Fundamentals", 25, "Types & functions;DOM;Async/await;ES modules", "javascript.info"),
            M("React & State Management", 30, "Components & props;Hooks;Routing;Forms", "react.dev Learn"),
            M("Backend APIs & Databases", 30, "REST design;Flask or Node;SQL;Authentication", "Flask Mega-Tutorial"),
            M("Testing & Deployment", 15, "Unit tests;CI/CD;Hosting;Performance", "The Odin Project"),
        ]},
    "Data Science": {
        "roles": ["Data Analyst", "Data Scientist", "BI Developer", "Data Engineer"],
        "skills": ["Python", "SQL", "Pandas", "Statistics", "Excel", "Tableau", "Power BI", "Machine Learning", "Visualization", "NumPy"],
        "modules": [
            M("Python, SQL & Excel", 20, "Python for data;SQL joins;Window functions;Excel pivots", "Mode SQL Tutorial"),
            M("Data Cleaning & EDA", 20, "Pandas;Missing data;Outliers;Visual exploration", "Kaggle Learn: Pandas"),
            M("Statistics & Experiments", 25, "Distributions;Hypothesis tests;A/B testing;Regression", "Khan Academy Statistics"),
            M("Predictive Modeling", 30, "Feature engineering;Scikit-learn;Cross-validation;Tuning", "Scikit-learn User Guide"),
            M("Dashboards & Storytelling", 15, "Tableau/Power BI;KPI design;Presenting insights", "Storytelling with Data"),
        ]},
    "Cybersecurity": {
        "roles": ["Security Analyst", "Penetration Tester", "SOC Analyst", "Security Engineer"],
        "skills": ["Networking", "Linux", "Cryptography", "OWASP", "Python", "Wireshark", "SIEM", "Penetration Testing", "Incident Response", "Firewalls"],
        "modules": [
            M("Networking & OS Fundamentals", 25, "TCP/IP;DNS & HTTP;Linux command line;Windows internals", "Professor Messer Network+"),
            M("Cryptography Basics", 15, "Hashing;Symmetric & asymmetric;TLS;PKI", "Cryptography I (Coursera)"),
            M("Web App Security (OWASP)", 25, "Injection;XSS & CSRF;Auth flaws;Secure coding", "OWASP Juice Shop"),
            M("Vulnerability Assessment", 25, "Nmap;Burp Suite;Reporting;Risk scoring", "TryHackMe Pre-Security"),
            M("Incident Response & SIEM", 20, "Log analysis;Detection rules;Playbooks;Forensics basics", "Blue Team Labs"),
        ]},
    "Cloud Computing": {
        "roles": ["Cloud Engineer", "Solutions Architect", "Cloud Security Engineer"],
        "skills": ["AWS", "Azure", "Linux", "Networking", "Terraform", "Docker", "Kubernetes", "Python", "IAM", "Serverless"],
        "modules": [
            M("Linux & Networking", 20, "Shell;Permissions;Subnets;Load balancing", "Linux Journey"),
            M("Cloud Fundamentals", 25, "Compute & storage;IAM;VPC;Pricing", "AWS Cloud Practitioner Essentials"),
            M("Containers with Docker", 15, "Images;Compose;Registries;Best practices", "Docker Get Started"),
            M("Infrastructure as Code", 20, "Terraform basics;State;Modules;Environments", "HashiCorp Learn"),
            M("Serverless & Architecture", 20, "Lambda;Event-driven design;Well-Architected;Cost control", "AWS Well-Architected"),
        ]},
    "Mobile Development": {
        "roles": ["Android Developer", "iOS Developer", "Flutter Developer", "React Native Developer"],
        "skills": ["Kotlin", "Swift", "Dart", "Flutter", "React Native", "Java", "REST", "Firebase", "Git", "SQLite"],
        "modules": [
            M("Language Fundamentals", 25, "Kotlin/Dart/Swift basics;OOP;Collections;Null safety", "Kotlin Koans / Dart Pad"),
            M("UI Layouts & Navigation", 25, "Widgets/Compose;Layouts;Navigation;Theming", "Flutter Codelabs"),
            M("State Management", 20, "State basics;Provider/ViewModel;Architecture", "Android Architecture Guide"),
            M("Networking & Storage", 20, "REST calls;JSON;SQLite/Room;Firebase", "Firebase Docs"),
            M("Publishing & Testing", 15, "Unit & UI tests;Signing;Play Store/App Store", "Google Play Console Help"),
        ]},
    "DevOps": {
        "roles": ["DevOps Engineer", "SRE", "Platform Engineer", "Release Engineer"],
        "skills": ["Linux", "Git", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Terraform", "Ansible", "Prometheus", "Python"],
        "modules": [
            M("Linux, Git & Scripting", 20, "Bash;Git workflows;Python scripting;Package managers", "Pro Git Book"),
            M("CI/CD Pipelines", 20, "GitHub Actions;Jenkins;Build & test;Artifacts", "GitHub Actions Docs"),
            M("Containers & Kubernetes", 30, "Docker;Pods & services;Helm;Scaling", "Kubernetes Basics"),
            M("Infrastructure as Code", 20, "Terraform;Ansible;Secrets;GitOps", "HashiCorp Learn"),
            M("Monitoring & Reliability", 20, "Prometheus;Grafana;SLOs;Incident postmortems", "Google SRE Book"),
        ]},
    "UI/UX Design": {
        "roles": ["UI Designer", "UX Designer", "Product Designer", "UX Researcher"],
        "skills": ["Figma", "Wireframing", "Prototyping", "User Research", "Typography", "Color Theory", "Accessibility", "Design Systems", "HTML", "CSS"],
        "modules": [
            M("Design Fundamentals", 20, "Typography;Color;Layout & grids;Visual hierarchy", "Refactoring UI"),
            M("Figma & Prototyping", 20, "Frames & auto layout;Components;Prototypes;Handoff", "Figma Learn"),
            M("User Research", 20, "Interviews;Surveys;Personas;Usability testing", "Nielsen Norman Group"),
            M("Interaction & Accessibility", 20, "Micro-interactions;WCAG;Inclusive design", "Inclusive Design Principles"),
            M("Portfolio & Case Studies", 25, "Case study structure;Design systems;Presenting work", "Google UX Design Certificate"),
        ]},
}

# title, company, location, salary, type, level, domain, description, skills
JOBS = [
    ("Machine Learning Engineer", "NeuralWorks", "Bengaluru", "₹12-20 LPA", "Full-time", "Junior", "AI & ML", "Build and deploy ML models for production recommendation systems.", ["Python", "PyTorch", "SQL", "Scikit-learn"]),
    ("NLP Intern", "LinguaAI", "Remote", "₹25k/month", "Internship", "Fresher", "AI & ML", "Work on text classification and chatbot pipelines.", ["Python", "NLP", "Pandas"]),
    ("Frontend Developer", "PixelForge", "Kochi", "₹5-9 LPA", "Full-time", "Fresher", "Web Development", "Create responsive React interfaces for client products.", ["React", "JavaScript", "CSS", "HTML"]),
    ("Full Stack Developer", "StackBridge", "Hyderabad", "₹10-18 LPA", "Full-time", "Mid", "Web Development", "Own features end to end across React and Flask services.", ["React", "Python", "Flask", "SQL", "REST"]),
    ("Data Analyst", "InsightLabs", "Chennai", "₹4-8 LPA", "Full-time", "Fresher", "Data Science", "Turn business data into dashboards and insights.", ["SQL", "Excel", "Tableau", "Python"]),
    ("Data Scientist", "Quantiva", "Pune", "₹14-24 LPA", "Full-time", "Mid", "Data Science", "Build predictive models and design experiments.", ["Python", "Statistics", "Machine Learning", "Pandas", "SQL"]),
    ("SOC Analyst", "ShieldOps", "Mumbai", "₹5-9 LPA", "Full-time", "Fresher", "Cybersecurity", "Monitor alerts and respond to security incidents.", ["SIEM", "Networking", "Incident Response", "Linux"]),
    ("Penetration Tester", "RedLine Security", "Remote", "₹10-16 LPA", "Contract", "Junior", "Cybersecurity", "Assess web apps and networks for vulnerabilities.", ["OWASP", "Penetration Testing", "Linux", "Python"]),
    ("Cloud Engineer", "SkyBase", "Bengaluru", "₹8-15 LPA", "Full-time", "Junior", "Cloud Computing", "Design and operate cloud infrastructure on AWS.", ["AWS", "Terraform", "Linux", "Networking"]),
    ("Solutions Architect", "NimbusWorks", "Gurugram", "₹25-40 LPA", "Full-time", "Senior", "Cloud Computing", "Lead cloud architecture for enterprise customers.", ["AWS", "Azure", "IAM", "Serverless", "Kubernetes"]),
    ("Android Developer", "AppNest", "Kochi", "₹6-12 LPA", "Full-time", "Junior", "Mobile Development", "Ship Kotlin apps used by millions.", ["Kotlin", "Java", "REST", "Firebase"]),
    ("Flutter Developer", "CrossPlat", "Remote", "₹5-10 LPA", "Full-time", "Fresher", "Mobile Development", "Build cross-platform apps with Flutter.", ["Dart", "Flutter", "Firebase", "Git"]),
    ("DevOps Engineer", "PipelineHQ", "Trivandrum", "₹8-14 LPA", "Full-time", "Junior", "DevOps", "Automate CI/CD and manage Kubernetes clusters.", ["Docker", "Kubernetes", "CI/CD", "Linux", "Git"]),
    ("Site Reliability Engineer", "UptimeLabs", "Bengaluru", "₹18-30 LPA", "Full-time", "Mid", "DevOps", "Keep services reliable with monitoring and automation.", ["Prometheus", "Terraform", "Python", "Kubernetes", "Linux"]),
    ("UI/UX Designer", "DesignHive", "Kochi", "₹4-8 LPA", "Full-time", "Fresher", "UI/UX Design", "Design web and mobile flows from research to prototype.", ["Figma", "Wireframing", "Prototyping", "User Research"]),
    ("Product Designer", "Fluent Studio", "Remote", "₹12-22 LPA", "Full-time", "Mid", "UI/UX Design", "Own design systems and ship polished product experiences.", ["Figma", "Design Systems", "Accessibility", "Prototyping", "Typography"]),
]

def C(domain, title, diff, desc, starter, tests, hints, solution):
    return dict(domain=domain, title=title, difficulty=diff, points={"easy": 10, "medium": 20, "hard": 30}[diff],
                description=desc, starter_code=starter, tests=[{"input": i, "expected": e} for i, e in tests], hints=hints, solution=solution)

CHALLENGES = [
    C("all", "Two Sum", "easy", "Given a list nums and an integer target, return indices [i, j] (i < j) of the two numbers that add up to target.",
      "def solution(nums, target):\n    pass\n", [([[2, 7, 11, 15], 9], [0, 1]), ([[3, 2, 4], 6], [1, 2]), ([[3, 3], 6], [0, 1])],
      ["Brute force checks every pair in O(n^2).", "Store each number's index in a dict as you scan.", "For each n, look up target - n in the dict."],
      "def solution(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n"),
    C("all", "Reverse String", "easy", "Return the reverse of string s.", "def solution(s):\n    pass\n",
      [(["hello"], "olleh"), ([""], ""), (["Ab c"], "c bA")], ["Strings support slicing.", "Try a step of -1."], "def solution(s):\n    return s[::-1]\n"),
    C("all", "Valid Parentheses", "medium", "Return True if the brackets in s (only ()[]{}) are closed in the correct order.", "def solution(s):\n    pass\n",
      [(["()[]{}"], True), (["(]"], False), (["([{}])"], True), (["(("], False)], ["Think of a stack.", "Push openers; on a closer, the top must be its match."],
      "def solution(s):\n    pairs = {')': '(', ']': '[', '}': '{'}\n    st = []\n    for c in s:\n        if c in pairs:\n            if not st or st.pop() != pairs[c]:\n                return False\n        else:\n            st.append(c)\n    return not st\n"),
    C("all", "Max Subarray Sum", "medium", "Return the largest sum of any contiguous, non-empty subarray of nums.", "def solution(nums):\n    pass\n",
      [([[-2, 1, -3, 4, -1, 2, 1, -5, 4]], 6), ([[1]], 1), ([[-3, -1, -2]], -1)], ["Track the best sum ending at each position.", "Kadane: cur = max(n, cur + n)."],
      "def solution(nums):\n    cur = best = nums[0]\n    for n in nums[1:]:\n        cur = max(n, cur + n)\n        best = max(best, cur)\n    return best\n"),
    C("AI & ML", "Dot Product", "easy", "Return the dot product of two equal-length lists a and b.", "def solution(a, b):\n    pass\n",
      [([[1, 2, 3], [4, 5, 6]], 32), ([[0, 0], [5, 9]], 0)], ["Multiply matching elements, then add.", "zip(a, b) pairs them up."], "def solution(a, b):\n    return sum(x * y for x, y in zip(a, b))\n"),
    C("AI & ML", "Min-Max Normalize", "medium", "Scale a list of numbers to the range 0-1 using (x - min) / (max - min), rounded to 2 decimals. If all values are equal return zeros.",
      "def solution(nums):\n    pass\n", [([[1, 2, 3]], [0.0, 0.5, 1.0]), ([[5, 5]], [0.0, 0.0]), ([[0, 10, 5]], [0.0, 1.0, 0.5])],
      ["Compute min and max first.", "Handle max == min separately."],
      "def solution(nums):\n    lo, hi = min(nums), max(nums)\n    if hi == lo:\n        return [0.0] * len(nums)\n    return [round((x - lo) / (hi - lo), 2) for x in nums]\n"),
    C("Data Science", "Mean of List", "easy", "Return the arithmetic mean of a non-empty list, rounded to 2 decimals.", "def solution(nums):\n    pass\n",
      [([[1, 2, 3, 4]], 2.5), ([[10]], 10), ([[1, 2]], 1.5)], ["sum() and len() help.", "Use round(value, 2)."], "def solution(nums):\n    return round(sum(nums) / len(nums), 2)\n"),
    C("Data Science", "Word Frequency", "medium", "Return a dict of word counts for text, lowercased, splitting on spaces.", "def solution(text):\n    pass\n",
      [(["a b a"], {"a": 2, "b": 1}), (["Hi hi HI"], {"hi": 3}), ([""], {})], ["Lowercase, then split().", "A dict with .get(w, 0) + 1 works."],
      "def solution(text):\n    out = {}\n    for w in text.lower().split():\n        out[w] = out.get(w, 0) + 1\n    return out\n"),
    C("Web Development", "Is Palindrome", "easy", "Return True if s reads the same backwards, ignoring case and non-alphanumeric characters.", "def solution(s):\n    pass\n",
      [(["A man, a plan, a canal: Panama"], True), (["hello"], False), ([""], True)], ["Filter with str.isalnum().", "Compare the cleaned string to its reverse."],
      "def solution(s):\n    t = [c.lower() for c in s if c.isalnum()]\n    return t == t[::-1]\n"),
    C("Cybersecurity", "Caesar Cipher", "medium", "Shift every lowercase letter in s forward by k (wrapping z to a). Leave other characters unchanged.", "def solution(s, k):\n    pass\n",
      [(["abc", 1], "bcd"), (["xyz", 3], "abc"), (["a b!", 2], "c d!")], ["ord() and chr() convert letters and numbers.", "Use modulo 26."],
      "def solution(s, k):\n    return ''.join(chr((ord(c) - 97 + k) % 26 + 97) if 'a' <= c <= 'z' else c for c in s)\n"),
    C("Cybersecurity", "Password Strength", "easy", "Return 'strong' if s has 8+ chars with an uppercase letter, lowercase letter and digit; otherwise 'weak'.", "def solution(s):\n    pass\n",
      [(["Abcdef12"], "strong"), (["abcdefgh"], "weak"), (["Ab1"], "weak")], ["Check length first.", "any(c.isupper() for c in s) is handy."],
      "def solution(s):\n    ok = len(s) >= 8 and any(c.isupper() for c in s) and any(c.islower() for c in s) and any(c.isdigit() for c in s)\n    return 'strong' if ok else 'weak'\n"),
    C("Cloud Computing", "Merge Intervals", "hard", "Merge overlapping [start, end] intervals and return them sorted by start.", "def solution(intervals):\n    pass\n",
      [([[[1, 3], [2, 6], [8, 10]]], [[1, 6], [8, 10]]), ([[[1, 4], [4, 5]]], [[1, 5]]), ([[]], [])], ["Sort by start first.", "Compare each interval's start with the last merged end."],
      "def solution(intervals):\n    out = []\n    for s, e in sorted(intervals):\n        if out and s <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], e)\n        else:\n            out.append([s, e])\n    return out\n"),
    C("DevOps", "Count Status Codes", "easy", "Given a list of HTTP status code integers, return a dict with counts of 'ok' (2xx), 'client_error' (4xx) and 'server_error' (5xx).", "def solution(codes):\n    pass\n",
      [([[200, 404, 500, 201]], {"ok": 2, "client_error": 1, "server_error": 1}), ([[]], {"ok": 0, "client_error": 0, "server_error": 0})], ["Start with a dict of zeros.", "Use c // 100 to get the class."],
      "def solution(codes):\n    out = {'ok': 0, 'client_error': 0, 'server_error': 0}\n    for c in codes:\n        k = {2: 'ok', 4: 'client_error', 5: 'server_error'}.get(c // 100)\n        if k:\n            out[k] += 1\n    return out\n"),
    C("Mobile Development", "FizzBuzz List", "easy", "Return a list of strings for 1..n: 'Fizz' for multiples of 3, 'Buzz' for 5, 'FizzBuzz' for both, else the number as a string.", "def solution(n):\n    pass\n",
      [([5], ["1", "2", "Fizz", "4", "Buzz"]), ([15], ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"])], ["Check 15 first.", "Use the % operator."],
      "def solution(n):\n    out = []\n    for i in range(1, n + 1):\n        out.append('FizzBuzz' if i % 15 == 0 else 'Fizz' if i % 3 == 0 else 'Buzz' if i % 5 == 0 else str(i))\n    return out\n"),
    C("UI/UX Design", "Hex to RGB", "easy", "Convert a hex color like '#FF8800' to a list [r, g, b].", "def solution(h):\n    pass\n",
      [(["#FF8800"], [255, 136, 0]), (["#000000"], [0, 0, 0])], ["Strip the '#'.", "int(x, 16) parses hexadecimal."], "def solution(h):\n    h = h.lstrip('#')\n    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]\n"),
]

Q = lambda cat, q, kw: {"category": cat, "question": q, "keywords": kw.split(",")}
INTERVIEW_QUESTIONS = [
    Q("HR", "Tell me about yourself and what led you to this career path.", "student,experience,project,interest,skills,learn,passion"),
    Q("HR", "Why should we hire you over other candidates?", "skills,value,contribute,team,experience,learn,results"),
    Q("HR", "What are your greatest strengths and one weakness you are improving?", "strength,weakness,improving,feedback,learned,practice"),
    Q("HR", "Where do you see yourself in five years?", "goal,growth,learning,leadership,skills,plan"),
    Q("HR", "Why do you want to work in this domain?", "interest,problem,impact,learn,future,curious"),
    Q("Technical", "Explain a technical project you built. What problem did it solve and which technologies did you use?", "problem,used,built,api,database,tested,result,deployed"),
    Q("Technical", "How do you approach debugging a problem you have never seen before?", "reproduce,logs,isolate,test,hypothesis,documentation,step"),
    Q("Technical", "What is the difference between a process and a thread, or a list and a tuple? Pick one and explain.", "difference,memory,mutable,shared,example,because"),
    Q("Technical", "How would you design a simple URL shortener?", "database,hash,api,scale,cache,collision,redirect"),
    Q("Technical", "How do you make sure your code is correct and maintainable?", "tests,review,readable,documentation,refactor,git,naming"),
    Q("Behavioral", "Describe a time you worked in a team and faced a disagreement. How did you handle it?", "team,listened,communicated,compromise,outcome,learned"),
    Q("Behavioral", "Tell me about a time you failed. What did you learn?", "failed,mistake,learned,improved,changed,responsibility"),
    Q("Behavioral", "Describe a time you met a tight deadline.", "deadline,prioritized,planned,delivered,communicated,result"),
    Q("Behavioral", "Tell me about a time you took initiative.", "initiative,noticed,proposed,led,impact,result"),
    Q("Behavioral", "Describe a situation where you had to learn something quickly.", "learned,resources,practice,applied,result,quickly"),
    Q("Situational", "Your teammate keeps missing deadlines and it affects your work. What do you do?", "talk,understand,support,escalate,communicate,solution"),
    Q("Situational", "You find a critical bug an hour before release. What do you do?", "assess,severity,inform,fix,rollback,test,communicate"),
    Q("Situational", "A client asks for a feature that is not possible in the timeline. How do you respond?", "explain,options,prioritize,scope,alternative,communicate"),
    Q("Situational", "You disagree with your manager's technical decision. What would you do?", "respect,data,discuss,listen,evidence,commit"),
    Q("Situational", "You are given a task with unclear requirements. How do you proceed?", "clarify,questions,assumptions,document,stakeholders,iterate"),
]

MENTORS = [
    {"id": 1, "name": "Priya Nair", "title": "Senior ML Engineer", "company": "NeuralWorks", "domain": "AI & ML", "experience": "9 years", "bio": "Helps freshers break into ML with project-first learning."},
    {"id": 2, "name": "Arjun Menon", "title": "Staff Software Engineer", "company": "StackBridge", "domain": "Web Development", "experience": "12 years", "bio": "Full stack architecture, code reviews and interview prep."},
    {"id": 3, "name": "Divya Raman", "title": "Lead Data Scientist", "company": "Quantiva", "domain": "Data Science", "experience": "8 years", "bio": "Analytics careers, portfolio reviews and SQL coaching."},
    {"id": 4, "name": "Rahul Verma", "title": "Security Consultant", "company": "ShieldOps", "domain": "Cybersecurity", "experience": "10 years", "bio": "Pathways into SOC and pentesting roles."},
    {"id": 5, "name": "Sneha Iyer", "title": "Cloud Architect", "company": "SkyBase", "domain": "Cloud Computing", "experience": "11 years", "bio": "AWS certifications and cloud career roadmaps."},
    {"id": 6, "name": "Kiran Das", "title": "Principal Product Designer", "company": "Fluent Studio", "domain": "UI/UX Design", "experience": "13 years", "bio": "Portfolio critiques and design interviews."},
]

EVENTS = [
    {"id": 1, "title": "Resume Teardown Live", "date": "Every Saturday, 6 PM IST", "mode": "Webinar", "description": "Live review of anonymous resumes with hiring managers."},
    {"id": 2, "title": "Mock Interview Marathon", "date": "First Sunday of the month", "mode": "Online", "description": "Back-to-back peer interviews with feedback rubrics."},
    {"id": 3, "title": "Intro to Cloud in 90 Minutes", "date": "Next Wednesday, 7 PM IST", "mode": "Webinar", "description": "Deploy your first app on AWS with a hands-on walkthrough."},
    {"id": 4, "title": "Campus to Career Q&A", "date": "Fortnightly Friday, 5 PM IST", "mode": "Webinar", "description": "Ask recent grads and mentors anything about breaking in."},
]
