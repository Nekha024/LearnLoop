"""
Groq AI Service for IT Career Prediction
Calls Groq's API with user answers and returns structured career predictions.
"""

import json
import logging
from groq import Groq
from django.conf import settings
import traceback
import httpx

logger = logging.getLogger(__name__)

# All possible IT career roles the system can predict
IT_CAREER_ROLES = [
    "Software Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Mobile App Developer",
    "UI/UX Designer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI/NLP Engineer",
    "Cybersecurity Analyst",
    "Ethical Hacker / Penetration Tester",
    "Network Engineer",
    "Cloud Engineer / DevOps",
    "Database Administrator",
    "IT Support Specialist",
    "Systems Administrator",
    "Game Developer",
    "Embedded Systems Engineer",
    "Blockchain Developer",
    "Product Manager (Tech)",
    "Scrum Master / Agile Coach",
    "Technical Writer",
    "IT Project Manager",
    "Business Analyst (IT)",
    "Tech Sales / Pre-Sales Engineer",
    "IT Consultant",
    "QA / Test Engineer",
    "Computer Vision Engineer",
    "Robotics / Automation Engineer",
    "NOT SUITABLE FOR IT FIELD",
]

ROADMAPS = {
    "Software Developer": {
        "description": "Software Developers design and build applications and systems. They write code to solve real-world problems and can specialize in various domains.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Learn Python or JavaScript basics", "Understand data structures & algorithms", "Practice on platforms like HackerRank or LeetCode"]},
            {"phase": "Core Skills (3–6 months)", "steps": ["Learn Git & version control", "Build 2-3 mini projects", "Understand OOP concepts"]},
            {"phase": "Specialization (6–12 months)", "steps": ["Pick a domain: web/mobile/backend", "Learn relevant frameworks (React, Django, Spring)", "Contribute to open-source"]},
            {"phase": "Job Ready (12–18 months)", "steps": ["Build a portfolio of 4-5 real projects", "Practice system design basics", "Apply for internships or entry-level roles"]},
        ]
    },
    "Frontend Developer": {
        "description": "Frontend Developers build the visual layer of websites and apps — everything users see and interact with. A mix of coding and design sense is key.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Master HTML5 and CSS3", "Learn JavaScript fundamentals", "Understand responsive design principles"]},
            {"phase": "Frameworks (3–6 months)", "steps": ["Learn React.js or Vue.js", "CSS frameworks (Tailwind, Bootstrap)", "Browser developer tools"]},
            {"phase": "Advanced (6–12 months)", "steps": ["TypeScript basics", "Performance optimization", "Accessibility & SEO fundamentals"]},
            {"phase": "Portfolio (12–18 months)", "steps": ["Build 5 real-world UI projects", "Deploy on Netlify/Vercel", "Contribute to design systems"]},
        ]
    },
    "Backend Developer": {
        "description": "Backend Developers build the server-side logic, databases, and APIs that power applications. They ensure data flows correctly behind the scenes.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Learn Python, Java, or Node.js", "Understand HTTP, APIs, and REST", "Learn SQL basics"]},
            {"phase": "Core Backend (3–6 months)", "steps": ["Pick a framework (Django, Spring Boot, Express)", "Learn database design (PostgreSQL/MySQL)", "Authentication and session management"]},
            {"phase": "Infrastructure (6–12 months)", "steps": ["Docker and containerization", "Caching (Redis)", "Message queues (RabbitMQ/Kafka)"]},
            {"phase": "Production Ready (12–18 months)", "steps": ["CI/CD pipelines", "Monitoring & logging", "Cloud deployment (AWS/GCP/Azure)"]},
        ]
    },
    "Full Stack Developer": {
        "description": "Full Stack Developers handle both frontend and backend development. They can build complete applications end-to-end.",
        "roadmap": [
            {"phase": "Foundation (0–4 months)", "steps": ["HTML, CSS, JavaScript", "Python or Node.js for backend", "Git & command line"]},
            {"phase": "Full Stack Basics (4–9 months)", "steps": ["React.js + REST APIs", "Database integration", "Authentication flows"]},
            {"phase": "Real Projects (9–15 months)", "steps": ["Build 3 full-stack projects", "Learn deployment (Heroku, Render, Railway)", "Understand DevOps basics"]},
            {"phase": "Senior Skills (15–24 months)", "steps": ["System design and scalability", "Microservices or serverless", "Technical interviews prep"]},
        ]
    },
    "Mobile App Developer": {
        "description": "Mobile App Developers create applications for Android and iOS devices. They focus on performance, UX, and platform-specific features.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Learn Dart (Flutter) or Kotlin/Swift", "Understand mobile UI principles", "Setup development environment"]},
            {"phase": "Core Development (3–8 months)", "steps": ["Build with Flutter or React Native", "State management (Provider, Redux)", "API integration"]},
            {"phase": "Advanced (8–14 months)", "steps": ["Push notifications, payments", "App store deployment", "Performance and battery optimization"]},
            {"phase": "Portfolio (14–18 months)", "steps": ["Publish 2 apps to Play Store/App Store", "Monetization strategies", "Reviews and iteration"]},
        ]
    },
    "UI/UX Designer": {
        "description": "UI/UX Designers create intuitive, accessible, and beautiful digital experiences. They bridge user needs and technical constraints.",
        "roadmap": [
            {"phase": "Foundation (0–2 months)", "steps": ["Learn Figma or Adobe XD", "Understand design principles (typography, color)", "Study UX research basics"]},
            {"phase": "Design Skills (2–6 months)", "steps": ["Wireframing and prototyping", "User research & testing", "Accessibility guidelines"]},
            {"phase": "Portfolio (6–12 months)", "steps": ["Redesign 3 existing apps (case studies)", "Build a Behance/Dribbble portfolio", "Learn motion design basics"]},
            {"phase": "Industry Ready (12–18 months)", "steps": ["Collaborate with developers", "Design systems (tokens, components)", "Land a junior designer role"]},
        ]
    },
    "Data Analyst": {
        "description": "Data Analysts collect, clean, and interpret data to help organizations make informed decisions. A combination of analytical thinking and visualization skills is essential.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Learn Excel and Google Sheets deeply", "SQL for databases", "Basic statistics and probability"]},
            {"phase": "Core Tools (3–6 months)", "steps": ["Python with Pandas and NumPy", "Data visualization (Matplotlib, Power BI, Tableau)", "Exploratory data analysis"]},
            {"phase": "Real Projects (6–12 months)", "steps": ["Analyze real datasets (Kaggle, UCI)", "Build dashboards for business problems", "Learn storytelling with data"]},
            {"phase": "Career (12–18 months)", "steps": ["Get Google Data Analytics Certificate", "Build a portfolio of 4-5 analysis projects", "Apply to analyst roles"]},
        ]
    },
    "Data Scientist": {
        "description": "Data Scientists extract insights from large datasets using statistics, machine learning, and programming. They turn raw data into actionable intelligence.",
        "roadmap": [
            {"phase": "Foundation (0–4 months)", "steps": ["Strong Python fundamentals", "Statistics and linear algebra", "Pandas, NumPy, Matplotlib"]},
            {"phase": "ML Basics (4–9 months)", "steps": ["Scikit-learn models (regression, classification)", "Feature engineering", "Kaggle competitions"]},
            {"phase": "Advanced ML (9–15 months)", "steps": ["Deep learning with TensorFlow/PyTorch", "NLP or Computer Vision specialization", "Model deployment (Flask/FastAPI)"]},
            {"phase": "Industry Ready (15–24 months)", "steps": ["End-to-end ML projects", "MLOps fundamentals", "Build Kaggle ranking and GitHub portfolio"]},
        ]
    },
    "Machine Learning Engineer": {
        "description": "ML Engineers build and deploy production-grade machine learning systems. They focus on scalability, efficiency, and model lifecycle management.",
        "roadmap": [
            {"phase": "Foundation (0–4 months)", "steps": ["Advanced Python", "Linear algebra and probability", "ML fundamentals (Andrew Ng's course)"]},
            {"phase": "ML Engineering (4–10 months)", "steps": ["Deep learning (PyTorch)", "Model training pipelines", "Cloud ML platforms (AWS SageMaker, GCP Vertex)"]},
            {"phase": "MLOps (10–18 months)", "steps": ["Docker and Kubernetes", "CI/CD for ML models", "Feature stores and monitoring"]},
            {"phase": "Expert (18–24 months)", "steps": ["Distributed training", "LLM fine-tuning", "Research paper implementations"]},
        ]
    },
    "Cybersecurity Analyst": {
        "description": "Cybersecurity Analysts protect organizations from digital threats. They monitor systems, identify vulnerabilities, and respond to incidents.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Networking fundamentals (TCP/IP, DNS, HTTP)", "Linux command line basics", "Security+ certification prep"]},
            {"phase": "Core Security (3–9 months)", "steps": ["SIEM tools (Splunk, IBM QRadar)", "Vulnerability scanning (Nessus, OpenVAS)", "Incident response basics"]},
            {"phase": "Specialization (9–18 months)", "steps": ["SOC analyst skills", "Threat intelligence", "OWASP Top 10 and web security"]},
            {"phase": "Certifications (18–24 months)", "steps": ["CompTIA Security+", "CEH or CCNA Security", "Build a home security lab"]},
        ]
    },
    "Ethical Hacker / Penetration Tester": {
        "description": "Ethical Hackers legally test systems for vulnerabilities before malicious hackers can exploit them. This role requires deep technical knowledge and strong ethics.",
        "roadmap": [
            {"phase": "Foundation (0–4 months)", "steps": ["Networking (TCP/IP, protocols)", "Linux and scripting (Bash, Python)", "Basic web technologies"]},
            {"phase": "Hacking Skills (4–10 months)", "steps": ["Kali Linux and hacking tools", "TryHackMe and HackTheBox challenges", "OWASP vulnerabilities"]},
            {"phase": "Advanced (10–18 months)", "steps": ["Metasploit framework", "Buffer overflow and exploit development", "Active Directory attacks"]},
            {"phase": "Certification (18–24 months)", "steps": ["CEH certification", "OSCP (gold standard)", "Build CTF portfolio and bug bounty history"]},
        ]
    },
    "Cloud Engineer / DevOps": {
        "description": "Cloud/DevOps Engineers build and manage scalable infrastructure. They automate deployment pipelines and ensure high availability of systems.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Linux administration", "Bash scripting", "Git and CI/CD basics"]},
            {"phase": "Cloud Basics (3–8 months)", "steps": ["AWS/GCP/Azure core services", "Docker containerization", "Infrastructure as Code (Terraform)"]},
            {"phase": "DevOps Tools (8–14 months)", "steps": ["Kubernetes orchestration", "Jenkins/GitHub Actions pipelines", "Monitoring (Prometheus, Grafana)"]},
            {"phase": "Certifications (14–24 months)", "steps": ["AWS Solutions Architect Associate", "Kubernetes CKA", "Cloud security fundamentals"]},
        ]
    },
    "Network Engineer": {
        "description": "Network Engineers design, implement, and maintain computer networks. From local offices to global infrastructure, they keep the internet running.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["OSI model and TCP/IP", "Subnetting and IP addressing", "Basic routing and switching"]},
            {"phase": "Core Networking (3–8 months)", "steps": ["Cisco CLI basics", "VLANs, STP, OSPF, BGP", "Firewall and NAT configuration"]},
            {"phase": "Advanced (8–14 months)", "steps": ["Network security and VPNs", "SDN and network automation (Python)", "Packet analysis (Wireshark)"]},
            {"phase": "Certification (14–18 months)", "steps": ["CCNA certification", "Network+ or JNCIA", "Build a home lab with Packet Tracer or GNS3"]},
        ]
    },
    "Database Administrator": {
        "description": "DBAs manage, secure, and optimize databases that store an organization's most valuable data. Precision and reliability are critical in this role.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["SQL fundamentals", "Database design and normalization", "Intro to PostgreSQL and MySQL"]},
            {"phase": "DBA Skills (3–8 months)", "steps": ["Backup and recovery strategies", "Performance tuning and indexing", "User roles and permissions"]},
            {"phase": "Advanced (8–14 months)", "steps": ["NoSQL databases (MongoDB, Redis)", "Replication and high availability", "Query optimization"]},
            {"phase": "Certifications (14–18 months)", "steps": ["Oracle Database Foundations", "Microsoft SQL Server certifications", "Cloud database services (AWS RDS, Cloud SQL)"]},
        ]
    },
    "IT Support Specialist": {
        "description": "IT Support Specialists help users with hardware and software problems. They are the frontline of any IT department and require broad, practical knowledge.",
        "roadmap": [
            {"phase": "Foundation (0–2 months)", "steps": ["Computer hardware basics", "Windows and Linux administration", "Troubleshooting methodologies"]},
            {"phase": "Core Skills (2–6 months)", "steps": ["Ticketing systems (Jira, ServiceNow)", "Active Directory and user management", "Networking basics"]},
            {"phase": "Growth (6–12 months)", "steps": ["Cloud tools (Microsoft 365, Google Workspace)", "Automation with PowerShell or scripts", "CompTIA A+ prep"]},
            {"phase": "Advance to L2/L3 (12–18 months)", "steps": ["CompTIA A+ certification", "Specialize in networking or security", "Aim for sysadmin or cloud roles"]},
        ]
    },
    "Game Developer": {
        "description": "Game Developers create interactive games across platforms. They combine programming with creativity and often specialize in gameplay, graphics, or physics.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["C# or C++ programming basics", "Unity or Unreal Engine intro", "2D game fundamentals"]},
            {"phase": "Core Development (3–9 months)", "steps": ["Physics, collision, and game loops", "2D/3D asset integration", "Game UI and menus"]},
            {"phase": "Intermediate (9–15 months)", "steps": ["Multiplayer basics (Photon, Mirror)", "Shaders and visual effects", "Optimization for mobile/PC"]},
            {"phase": "Portfolio (15–24 months)", "steps": ["Publish to itch.io or Steam", "Participate in Game Jams", "Build playable demo portfolio"]},
        ]
    },
    "Product Manager (Tech)": {
        "description": "Tech Product Managers bridge business and technology. They define product vision, prioritize features, and guide development teams to build the right things.",
        "roadmap": [
            {"phase": "Foundation (0–2 months)", "steps": ["Product thinking basics", "Agile and Scrum methodology", "User story writing"]},
            {"phase": "Core PM Skills (2–6 months)", "steps": ["Roadmapping and prioritization frameworks", "Basic data analysis for decisions", "Stakeholder communication"]},
            {"phase": "Tools & Practice (6–12 months)", "steps": ["Jira, Notion, Figma basics", "A/B testing concepts", "Competitive analysis techniques"]},
            {"phase": "Career (12–18 months)", "steps": ["Build a product management case study portfolio", "Associate PM programs (Google, Microsoft, Meta)", "Product management certifications"]},
        ]
    },
    "Technical Writer": {
        "description": "Technical Writers create documentation, tutorials, and guides for software and products. They make complex tech understandable for diverse audiences.",
        "roadmap": [
            {"phase": "Foundation (0–2 months)", "steps": ["Strong English writing and grammar", "Learn Markdown and basic HTML", "Understand software development lifecycle"]},
            {"phase": "Core Skills (2–6 months)", "steps": ["API documentation basics", "Tools: Confluence, Notion, Gitbook", "Writing user guides and tutorials"]},
            {"phase": "Technical Skills (6–12 months)", "steps": ["Version control with Git", "Learn REST API concepts", "Docs-as-code workflows"]},
            {"phase": "Portfolio (12–18 months)", "steps": ["Contribute to open-source documentation", "Build a technical writing portfolio", "Apply to developer relations or docs roles"]},
        ]
    },
    "QA / Test Engineer": {
        "description": "QA Engineers ensure software quality by designing and executing tests. They catch bugs before users do and are essential to reliable software delivery.",
        "roadmap": [
            {"phase": "Foundation (0–2 months)", "steps": ["Software testing fundamentals", "Test case and bug report writing", "Manual testing basics"]},
            {"phase": "Automation (2–8 months)", "steps": ["Python or Java for test scripts", "Selenium WebDriver", "Postman for API testing"]},
            {"phase": "Advanced Testing (8–14 months)", "steps": ["CI/CD integration with testing", "Performance testing (JMeter)", "Security testing basics"]},
            {"phase": "Certifications (14–18 months)", "steps": ["ISTQB Foundation Level", "Cypress or Playwright for modern testing", "Apply for SDET roles"]},
        ]
    },
    "IT Consultant": {
        "description": "IT Consultants advise businesses on technology strategy, implementation, and optimization. They need both technical depth and strong business acumen.",
        "roadmap": [
            {"phase": "Foundation (0–3 months)", "steps": ["Broad IT fundamentals", "Business communication and presentation", "Excel, PowerPoint, project tools"]},
            {"phase": "Domain Knowledge (3–9 months)", "steps": ["Pick specialization (ERP, cloud, cybersecurity)", "Learn consulting frameworks", "Case study analysis practice"]},
            {"phase": "Experience (9–18 months)", "steps": ["Freelance small projects", "Certifications in your domain", "Build a client portfolio"]},
            {"phase": "Growth (18–30 months)", "steps": ["Join consulting firm or go independent", "Build industry network", "Develop thought leadership online"]},
        ]
    },
    "Business Analyst (IT)": {
        "description": "IT Business Analysts translate business requirements into technical solutions. They act as communicators between stakeholders and development teams.",
        "roadmap": [
            {"phase": "Foundation (0–2 months)", "steps": ["Business process modeling", "Requirements gathering techniques", "UML and flowcharts"]},
            {"phase": "Core BA Skills (2–8 months)", "steps": ["Agile/Scrum for BAs", "User story and acceptance criteria writing", "SQL for data queries"]},
            {"phase": "Tools (8–14 months)", "steps": ["Jira, Confluence, Visio", "Process improvement methodologies (BPMN)", "Stakeholder management"]},
            {"phase": "Certifications (14–18 months)", "steps": ["ECBA or CCBA (IIBA certifications)", "Scrum certification", "Build BA project portfolio"]},
        ]
    },
    "NOT SUITABLE FOR IT FIELD": {
        "description": "Based on your responses, a traditional IT career might not be the best fit right now. This doesn't mean you can't work with technology — it means your strengths may lie elsewhere.",
        "roadmap": [
            {"phase": "Self-Discovery (0–2 months)", "steps": ["Take aptitude tests (Holland Codes, MBTI)", "List what genuinely excites you", "Talk to professionals in fields you like"]},
            {"phase": "Explore Adjacent Fields (2–6 months)", "steps": ["Digital marketing (uses tech but focuses on communication)", "Healthcare administration with tech tools", "Education and e-learning content creation"]},
            {"phase": "Leverage Tech as a Tool (6–12 months)", "steps": ["Learn tools like Canva, Notion, or CRM software", "Use data analytics for your chosen field", "Automation tools like Zapier or Make"]},
            {"phase": "Build Your Path (12–18 months)", "steps": ["Commit to a non-IT career aligned with your strengths", "Use technology as an enabler, not as the career itself", "Explore entrepreneurship in a non-tech domain using digital tools"]},
        ]
    },
}

# Add generic roadmaps for any role not explicitly defined
for role in IT_CAREER_ROLES:
    if role not in ROADMAPS:
        ROADMAPS[role] = {
            "description": f"{role} is a growing and in-demand IT career that combines technical skills with domain expertise.",
            "roadmap": [
                {"phase": "Foundation (0–3 months)", "steps": ["Research the role and its requirements", "Take beginner online courses", "Build foundational programming or technical skills"]},
                {"phase": "Skill Building (3–9 months)", "steps": ["Complete a structured learning path", "Work on hands-on projects", "Join communities in this domain"]},
                {"phase": "Experience (9–18 months)", "steps": ["Internship or freelance projects", "Build a portfolio or GitHub profile", "Earn a relevant entry-level certification"]},
                {"phase": "Career Launch (18–24 months)", "steps": ["Apply for junior-level positions", "Network with professionals on LinkedIn", "Continue specialized learning"]},
            ]
        }


def build_prediction_prompt(answers: dict) -> str:
    """Build the prompt for Groq with all 30 answers."""
    from .questions import QUESTIONS

    qa_lines = []
    for q in QUESTIONS:
        q_id = str(q["id"])
        answer_value = answers.get(q_id, "")
        # Find the label for the selected answer
        answer_label = answer_value
        for opt in q["options"]:
            if opt["value"] == answer_value:
                answer_label = opt["label"]
                break
        qa_lines.append(f"Q{q['id']} [{q['category']}]: {q['text']}\nAnswer: {answer_label}")

    questions_text = "\n\n".join(qa_lines)

    roles_list = "\n".join(f"- {r}" for r in IT_CAREER_ROLES)

    prompt = f"""You are an expert IT career counselor. Based on the 30 assessment answers below, predict the top 3 most suitable IT career roles for this person.

AVAILABLE CAREER ROLES:
{roles_list}

ASSESSMENT ANSWERS:
{questions_text}

INSTRUCTIONS:
1. Analyze ALL answers holistically — personality, interests, skills, goals, and background.
2. Consider if the person has NO technical background yet — if so, focus on aptitude, interest, and learning path.
3. Include "NOT SUITABLE FOR IT FIELD" as an option only if genuinely warranted.
4. For each of the 3 roles, provide a fit score (0-100) and a 2-sentence personalized explanation.

RESPOND IN VALID JSON ONLY — no extra text, no markdown fences. Format:
{{
  "top_careers": [
    {{
      "rank": 1,
      "role": "exact role name from list",
      "score": 85,
      "reason": "Two-sentence personalized explanation based on their specific answers."
    }},
    {{
      "rank": 2,
      "role": "exact role name from list",
      "score": 74,
      "reason": "Two-sentence personalized explanation."
    }},
    {{
      "rank": 3,
      "role": "exact role name from list",
      "score": 65,
      "reason": "Two-sentence personalized explanation."
    }}
  ],
  "overall_summary": "3-4 sentence summary of the person's profile and IT readiness."
}}"""
    return prompt


def get_career_prediction(answers: dict) -> dict:
    """Call Groq API and return structured prediction results."""
    prompt = build_prediction_prompt(answers)
    try:

        client = Groq(
            api_key=settings.GROQ_API_KEY,
            timeout=30.0  # Give it more time if your connection is slow
        )
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert IT career counselor. You MUST respond with a valid JSON object matching the requested schema."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2, 
            max_tokens=3000,
        )

        raw_response = completion.choices[0].message.content.strip()

        # Robust JSON extraction: Find the first '{' and the last '}'
        import re
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
        else:
            # Fallback to the original stripping logic
            json_str = raw_response
            if json_str.startswith("```"):
                json_str = json_str.strip("`").strip()
                if json_str.startswith("json"):
                    json_str = json_str[4:].strip()

        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            # Final attempt: remove common problematic characters like trailing commas before closing braces
            json_str_fixed = re.sub(r',\s*([\]}])', r'\1', json_str)
            result = json.loads(json_str_fixed)

        result["raw"] = raw_response

        # Attach roadmap + description for each career
        for career in result.get("top_careers", []):
            role = career["role"]
            if role in ROADMAPS:
                career["description"] = ROADMAPS[role]["description"]
                career["roadmap"] = ROADMAPS[role]["roadmap"]
            else:
                # Fallback
                career["description"] = f"A rewarding IT career path aligned with your profile."
                career["roadmap"] = []

        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error from Groq: {e}\nRaw: {raw_response}")
        return {"error": "Failed to parse AI response. Please try again.", "raw": raw_response}
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return {"error": f"AI service error: {str(e)}"}
    
    except Exception as e:
        print(traceback.format_exc()) # This will show the full error in your terminal
        logger.error(f"Groq API error: {str(e)}")
        return {"error": "Connection failed. Please check your network."}
