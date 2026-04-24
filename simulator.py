"""
Day-in-the-Life Simulator — Career Intelligence Engine v3.3
BRANCH_INTRO completely redesigned for 12th-standard students:
  - real_apps:        Everyday apps/products they use → what this branch built
  - bridge_12th:      Their 12th knowledge mapped to engineering superpowers
  - real_problems:    3 real before/after problem stories (no jargon)
  - personality_fit:  "You'll love this if..." statements
  - day_timeline:     Clickable hourly schedule
  - tools:            Tools list
  - reality_check:    The honest truth nobody tells you
  - youtube_search:   YouTube search query (always reliable)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
# Branch introductions  — redesigned for students with zero prior knowledge
# ─────────────────────────────────────────────────────────────────────────────

BRANCH_INTRO: Dict[str, Dict] = {

    "CSE": {
        "tagline": "Every tap on your phone runs code that someone like you wrote.",
        "real_apps": [
            {
                "app": "Zomato",
                "emoji": "🍕",
                "what_they_built": "When you tap 'Order', a backend engineer's code finds nearby restaurants, calculates ETAs, routes the order to the right kitchen, and charges your UPI — all in under 200ms.",
                "cool_fact": "Zomato's backend handles 1.5 lakh orders per hour during peak time. One bug can lose them ₹10 lakh in minutes."
            },
            {
                "app": "Google Maps",
                "emoji": "🗺️",
                "what_they_built": "The algorithm that finds the fastest route between two points across an entire country — considering 200 million road segments — runs in under 1 second. A CSE engineer designed that algorithm.",
                "cool_fact": "Google Maps processes 1 billion km of directions every day."
            },
            {
                "app": "UPI / PhonePe",
                "emoji": "💳",
                "what_they_built": "Every time money moves between bank accounts in India in 2 seconds flat — that's a distributed systems engineer's work. They ensure the money never disappears between accounts even if a server crashes mid-transfer.",
                "cool_fact": "UPI processes 10 billion transactions per month. Each one must be 100% accurate."
            },
            {
                "app": "Your Android phone",
                "emoji": "📱",
                "what_they_built": "The operating system that manages every app, every notification, every photo — 70% of all phones run Android, which is open-source software maintained by thousands of CSE engineers worldwide.",
                "cool_fact": "Android has 2.5 billion active users. The codebase has over 13 million lines of code."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Solving algebra problems step by step",
                "becomes_in_engineering": "Algorithm design — breaking any problem into logical steps a computer can execute",
                "emoji": "📐"
            },
            {
                "knew_in_12th": "Maths: sets, functions, logic gates",
                "becomes_in_engineering": "Data structures and discrete mathematics — the foundation of all programming",
                "emoji": "🔢"
            },
            {
                "knew_in_12th": "Computer Science class: if-else, loops, arrays",
                "becomes_in_engineering": "Writing production code used by millions — same concepts, infinitely bigger scale",
                "emoji": "💻"
            },
            {
                "knew_in_12th": "Physics: understanding how electricity flows in circuits",
                "becomes_in_engineering": "Understanding how hardware works — makes you a better systems programmer",
                "emoji": "⚡"
            },
        ],
        "real_problems": [
            {
                "problem": "In 2020, Zoom crashed for 300 million users on the same day.",
                "why_it_happened": "Their database couldn't handle the sudden load when the whole world switched to remote work overnight.",
                "how_engineers_fixed_it": "CSE engineers redesigned the database architecture to be distributed across hundreds of servers — so even if 10 servers fail, the app keeps running.",
                "lesson": "This is called 'distributed systems design' — one of the highest-paying skills in software.",
                "emoji": "🔧"
            },
            {
                "problem": "In 2019, a bank's online portal crashed and 2 lakh customers couldn't access their money for 3 days.",
                "why_it_happened": "A software update had a bug that corrupted the authentication system.",
                "how_engineers_fixed_it": "Now banks have 'canary deployments' — engineers release updates to 1% of users first. If something breaks, they catch it before it affects everyone.",
                "lesson": "This is 'DevOps engineering' — building systems so software updates are safe and automatic.",
                "emoji": "🏦"
            },
            {
                "problem": "Early ride-sharing apps in India assigned drivers randomly — sometimes a driver 15 km away when there was one 200m from you.",
                "why_it_happened": "The matching algorithm was too simple.",
                "how_engineers_fixed_it": "CSE engineers built a geospatial matching system that considers distance, traffic, driver rating, and ETA simultaneously — now Ola/Uber matching is nearly perfect.",
                "lesson": "Algorithm design changes actual user experience for millions of people.",
                "emoji": "🚕"
            },
        ],
        "personality_fit": [
            "You spend 10 minutes finding the 'cleanest' solution to a problem instead of the first one that works",
            "You get genuinely annoyed when an app is slow or crashes",
            "You've ever wondered how Instagram knows what you want to see before you do",
            "You enjoy puzzles, Sudoku, or anything where logic leads to a satisfying answer",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Check overnight alerts", "detail": "A payment API is failing for 0.2% of requests. You open the server logs to investigate.", "mood": "detective"},
            {"time": "10:00 AM", "task": "Team standup (15 min)", "detail": "5 people, everyone says what they did yesterday and what they're doing today. Fast and focused.", "mood": "team"},
            {"time": "10:30 AM", "task": "Deep work: debugging", "detail": "You trace the payment bug to a race condition — two requests running at the same time stepping on each other. You write a fix.", "mood": "focus"},
            {"time": "1:00 PM", "task": "Lunch break", "detail": "30-60 minutes. Most engineers step away from screens — it genuinely helps with problem-solving.", "mood": "break"},
            {"time": "2:00 PM", "task": "Code review", "detail": "A colleague's new feature has a potential security vulnerability. You leave a detailed comment explaining the risk and how to fix it.", "mood": "team"},
            {"time": "3:30 PM", "task": "Architecture meeting", "detail": "Your team is planning a new notifications system. You draw diagrams showing how data flows between services.", "mood": "creative"},
            {"time": "5:00 PM", "task": "Deploy & verify", "detail": "Your bug fix goes to production. You watch the error rate drop to 0% in real-time. Deeply satisfying.", "mood": "win"},
        ],
        "tools": ["Python / Java / Go", "VS Code / IntelliJ", "Git + GitHub", "AWS / GCP", "Docker & Kubernetes", "Postman (API testing)", "Datadog (monitoring)"],
        "reality_check": "You will spend 30% of your time reading other people's old, messy code. That's normal — senior engineers are good at it, not frustrated by it. The '10x programmer' who codes alone all day is a myth. Real engineering is collaborative.",
        "salary_snapshot": "Fresher at product company: ₹8–18 LPA. After 5 years at a top startup/MNC: ₹35–80 LPA.",
        "youtube_search": "day in the life software engineer India",
        
    },

    "CSE-AIML": {
        "tagline": "The algorithm that decides what you watch next, what ad you see, and whether your loan is approved — an ML engineer trained it.",
        "real_apps": [
            {
                "app": "Instagram / YouTube Reels",
                "emoji": "📱",
                "what_they_built": "Every video that appears on your feed was chosen by a recommendation model. It learned from watching 2 billion people's behaviour — what they watch, rewatch, skip, share. An ML engineer trained and maintains that model.",
                "cool_fact": "YouTube's recommendation system drives 70% of all watch time. It was not programmed — it learned."
            },
            {
                "app": "Google Translate",
                "emoji": "🌐",
                "what_they_built": "Google Translate supports 133 languages. Nobody manually wrote translation rules for all of them. An NLP engineer trained a model on billions of text pairs and the model figured out grammar, idioms, and context by itself.",
                "cool_fact": "The model can now translate between two languages it has never seen paired together."
            },
            {
                "app": "Your phone's camera",
                "emoji": "📷",
                "what_they_built": "Portrait mode, night mode, removing blur from moving subjects, recognising faces — all of these are computer vision models. An ML engineer trained them on millions of photos.",
                "cool_fact": "iPhone's photo processing runs 1 trillion operations per photo using an on-device AI chip."
            },
            {
                "app": "ChatGPT / Gemini",
                "emoji": "🤖",
                "what_they_built": "The large language models behind AI chatbots were trained by ML engineers on terabytes of text. The training alone took thousands of GPUs running for months.",
                "cool_fact": "GPT-4 was trained on roughly 45 terabytes of text — about 1/6th of all text ever published on the internet."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Statistics: mean, standard deviation, probability distributions",
                "becomes_in_engineering": "The foundation of every ML model — you use probability to measure how 'confident' a model is in its predictions",
                "emoji": "📊"
            },
            {
                "knew_in_12th": "Maths: matrices, linear algebra (vectors, dot products)",
                "becomes_in_engineering": "How neural networks store knowledge — millions of numbers in matrices multiplied together to produce intelligence",
                "emoji": "🔢"
            },
            {
                "knew_in_12th": "Calculus: derivatives, rates of change",
                "becomes_in_engineering": "Gradient descent — how an ML model learns by calculating which direction to move to reduce its errors",
                "emoji": "📉"
            },
            {
                "knew_in_12th": "Programming: loops, conditions, functions",
                "becomes_in_engineering": "Python for ML — you write the training code, data pipelines, and deployment scripts",
                "emoji": "🐍"
            },
        ],
        "real_problems": [
            {
                "problem": "Doctors miss 20% of early-stage cancers in X-ray scans — because human eyes get tired and X-rays are subtle.",
                "why_it_happened": "Early cancer looks almost identical to normal tissue. Even expert radiologists disagree on borderline cases.",
                "how_engineers_fixed_it": "ML engineers trained a computer vision model on 1 million labelled X-rays. The model now detects early cancer with 94% accuracy and never gets tired. It has saved thousands of lives.",
                "lesson": "This is 'medical AI' — one of the most impactful and well-funded areas in ML right now.",
                "emoji": "🏥"
            },
            {
                "problem": "Banks were losing ₹1,000 crore per year to credit card fraud — human fraud analysts couldn't review every transaction in time.",
                "why_it_happened": "Millions of transactions happen every second. Manual review is too slow.",
                "how_engineers_fixed_it": "ML engineers built a fraud detection model that analyses every transaction in 50 milliseconds — checking location, merchant type, amount, and pattern against previous behaviour — and flags suspicious ones automatically.",
                "lesson": "This is 'real-time ML' — models that make decisions faster than any human ever could.",
                "emoji": "💳"
            },
            {
                "problem": "Farmers in India lose 30% of crops to pests they don't detect early enough.",
                "why_it_happened": "A farmer with 10 acres cannot inspect every plant daily. By the time pest damage is visible, it's too late.",
                "how_engineers_fixed_it": "An ML engineer built an app: take a photo of a leaf, and the AI identifies the pest or disease in 2 seconds, with treatment recommendations in Hindi. Used by 4 million farmers now.",
                "lesson": "ML is not just for tech companies — it's solving India-specific problems that affect hundreds of millions of people.",
                "emoji": "🌾"
            },
        ],
        "personality_fit": [
            "You've wondered 'how does Spotify know I'd like this song I've never heard?'",
            "You enjoy finding patterns — in data, in behaviour, in how things work",
            "You're comfortable with maths and actually find statistics interesting",
            "You like experiments — trying different approaches and measuring which works best",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Check model metrics", "detail": "The fraud detection model's precision dropped 2% overnight. You open the dashboard to investigate what changed.", "mood": "detective"},
            {"time": "10:00 AM", "task": "Data exploration", "detail": "You load yesterday's transactions into a Jupyter notebook. Plot distributions. A new merchant category was added — the model has never seen it.", "mood": "research"},
            {"time": "11:30 AM", "task": "Retrain the model", "detail": "Include the new data, retrain, compare metrics. New model: +4% recall, same precision. You've improved the model without touching a line of the model code.", "mood": "focus"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "Walk outside if possible. Your brain solves problems in the background when you're not staring at a screen.", "mood": "break"},
            {"time": "2:00 PM", "task": "Code review", "detail": "A colleague's feature has a data leakage bug — they're accidentally using future data to train the model. You catch it before it ships.", "mood": "team"},
            {"time": "3:30 PM", "task": "Experiment: try new approach", "detail": "You test a gradient boosted model against the current neural net. Log all results in MLflow so you can compare later.", "mood": "creative"},
            {"time": "5:30 PM", "task": "Write up findings", "detail": "Document what you tried, what worked, and why. Good ML engineers are also good writers — reproducibility matters.", "mood": "win"},
        ],
        "tools": ["Python (NumPy, Pandas, PyTorch)", "Jupyter Notebook", "MLflow / W&B (experiment tracking)", "SQL + Spark (big data)", "Hugging Face (pre-trained models)", "Docker + Kubernetes", "AWS SageMaker / GCP Vertex AI"],
        "reality_check": "60–70% of your time is spent on data — cleaning it, understanding it, fixing broken pipelines. Only 10% is actually training models. The most important skill is not knowing fancy algorithms — it's knowing which simple one to try first.",
        "salary_snapshot": "Fresher: ₹10–20 LPA. Senior ML engineer after 5 years: ₹40–100 LPA. AI is the highest-paying engineering specialisation globally.",
        "youtube_search": "day in the life machine learning engineer",
        
    },

    "MECH": {
        "tagline": "Every physical thing you trust with your life — your car's brakes, the aircraft you fly in, the building you sit in — a mechanical engineer designed it.",
        "real_apps": [
            {
                "app": "Your bike / car / Activa",
                "emoji": "🚗",
                "what_they_built": "Every component was designed by mechanical engineers — the frame that doesn't crack when you hit a pothole, the engine that converts fuel to motion, the brakes that stop you in 4 metres at 60 km/h without fail. Each was simulated thousands of times before a single prototype was built.",
                "cool_fact": "Tata Nexon survived a 5-star NCAP crash test — the cabin stayed intact at 64 km/h impact. That's mechanical engineering."
            },
            {
                "app": "Air conditioning (everywhere)",
                "emoji": "❄️",
                "what_they_built": "A mechanical engineer designed the refrigeration cycle, the compressor, the heat exchanger, and the airflow system that keeps your classroom at 24°C when it's 45°C outside. HVAC is one of the most in-demand mechanical engineering fields in India.",
                "cool_fact": "Pune's IT parks use 15% of Maharashtra's industrial electricity — mostly for cooling servers and offices."
            },
            {
                "app": "ISRO rockets",
                "emoji": "🚀",
                "what_they_built": "The Chandrayaan-3 lander's legs were designed to absorb the impact of landing on the Moon at 2 m/s without breaking. Mechanical engineers calculated the exact alloy, thickness, and angle of each leg using finite element analysis.",
                "cool_fact": "ISRO employs 16,000 engineers — majority are mechanical and aerospace engineers."
            },
            {
                "app": "Factory robots (making your phone)",
                "emoji": "🤖",
                "what_they_built": "The robot arms that assemble your iPhone do so with 0.01mm precision, 20 hours a day, 365 days a year. Mechanical engineers designed the arm kinematics, the grippers, and the torque limits that prevent them from accidentally crushing a ₹80,000 phone.",
                "cool_fact": "Apple's Foxconn factory has 200,000 robots — each one was mechanically designed and programmed."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Physics: Newton's laws, forces, motion, friction",
                "becomes_in_engineering": "Engineering Mechanics — calculating whether a bridge, car frame, or rocket nozzle will survive the forces acting on it",
                "emoji": "⚖️"
            },
            {
                "knew_in_12th": "Physics: heat, thermodynamics, laws of heat transfer",
                "becomes_in_engineering": "Designing engines, cooling systems, heat exchangers — anything involving energy conversion",
                "emoji": "🌡️"
            },
            {
                "knew_in_12th": "Maths: calculus, integration, differential equations",
                "becomes_in_engineering": "Structural analysis and fluid dynamics — the maths that predicts how materials deform and how fluids flow",
                "emoji": "📐"
            },
            {
                "knew_in_12th": "Engineering Drawing / technical drawing class",
                "becomes_in_engineering": "CAD software (SolidWorks, CATIA) — the same thinking, but in 3D on a computer with millimetre-level precision",
                "emoji": "✏️"
            },
        ],
        "real_problems": [
            {
                "problem": "Early electric vehicles in India had batteries that swelled, overheated, and sometimes caught fire in summer.",
                "why_it_happened": "Lithium-ion batteries degrade rapidly above 45°C. Indian summers regularly hit 48°C. Nobody had designed the thermal management properly.",
                "how_engineers_fixed_it": "Mechanical engineers designed active liquid cooling systems — channels filled with glycol-water coolant running between battery cells, like a radiator for your battery. The Tata Nexon EV now operates safely at 50°C ambient.",
                "lesson": "This is 'thermal management' — one of the fastest-growing fields in EV engineering in India.",
                "emoji": "🔋"
            },
            {
                "problem": "A suspension bracket on a production car was failing after 80,000 km — causing dangerous wobble at highway speeds.",
                "why_it_happened": "A sharp corner in the bracket design created a stress concentration point — the metal fatigued and cracked there predictably.",
                "how_engineers_fixed_it": "Running FEA (Finite Element Analysis) revealed the exact failure point. Adding a 3mm fillet (rounded corner) at that point distributed the stress across a larger area. The part now lasts 200,000 km. Cost to fix: ₹12 per part.",
                "lesson": "Sometimes a ₹12 change in geometry prevents a ₹50,000 recall. This is why FEA is the most valued skill in mechanical engineering.",
                "emoji": "🔩"
            },
            {
                "problem": "A chemical plant's heat exchanger was running at 75% efficiency instead of the designed 95% — costing ₹2 crore per year in wasted energy.",
                "why_it_happened": "Nobody had cleaned it for 18 months. Mineral deposits had coated the heat transfer surfaces, acting as insulation.",
                "how_engineers_fixed_it": "A maintenance schedule was implemented. The engineer also redesigned the water treatment system to prevent deposits. Efficiency restored. Annual savings: ₹1.8 crore.",
                "lesson": "Mechanical engineering is not just design — maintenance and operational optimisation are equally valued.",
                "emoji": "🏭"
            },
        ],
        "personality_fit": [
            "You enjoy taking things apart to understand how they work — and actually putting them back together",
            "You've wondered how a car engine works, or why a plane doesn't fall out of the sky",
            "You like drawing, building, making physical things — not just looking at a screen",
            "You find satisfaction in something that works in the real world — not just on a computer",
        ],
        "day_timeline": [
            {"time": "8:30 AM", "task": "Factory floor inspection", "detail": "A suspension bracket keeps failing after 5,000 assembly cycles. You go to the floor and inspect the physical parts — looking for patterns in where they crack.", "mood": "detective"},
            {"time": "9:30 AM", "task": "FEA simulation", "detail": "Back at your desk. Open ANSYS, apply the exact forces measured on the floor. The simulation highlights a stress concentration at a sharp corner. Found it.", "mood": "research"},
            {"time": "11:00 AM", "task": "Design review", "detail": "Present FEA results to the team. Propose adding a fillet radius. Everyone agrees. You update the drawing in SolidWorks.", "mood": "team"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "Factory cafeteria. Most manufacturing engineers eat with the production team — you learn more about real problems at lunch than in meetings.", "mood": "break"},
            {"time": "2:00 PM", "task": "Update drawing & send to workshop", "detail": "Revise the SolidWorks model, generate engineering drawings with tolerances, send to the workshop. A prototype will be ready in 3 days.", "mood": "focus"},
            {"time": "3:30 PM", "task": "Vendor call", "detail": "Review material test certificates for a new aluminium alloy. Check tensile strength, yield strength, and elongation against your design requirements.", "mood": "research"},
            {"time": "5:00 PM", "task": "Documentation", "detail": "Update the design change log. Every engineering change is documented — future engineers (or lawyers, if something fails) need to understand what was changed and why.", "mood": "win"},
        ],
        "tools": ["SolidWorks / CATIA / AutoCAD (3D modelling)", "ANSYS (stress, thermal, fluid simulation)", "MATLAB / Simulink (dynamics & control)", "GD&T (technical drawing standards)", "Excel / Python (data analysis)", "PLM software (managing design files)"],
        "reality_check": "The first 2 years are often repetitive — updating drawings, running standardised tests, writing reports. This is normal and necessary. Senior mech engineers who can also simulate (FEA/CFD) and code Python are extremely rare and very highly paid. That combination is your goal.",
        "salary_snapshot": "Fresher at core company: ₹4–8 LPA. Senior engineer at Bosch / ISRO / Tata after 7 years: ₹18–35 LPA. EV sector is paying significantly more now.",
        "youtube_search": "day in the life mechanical engineer",
        
    },

    "ECE": {
        "tagline": "The chip inside your phone, the antenna on the tower giving you 5G, the sensor in your smartwatch — an electronics engineer designed them.",
        "real_apps": [
            {
                "app": "Your smartphone's processor",
                "emoji": "📱",
                "what_they_built": "The Snapdragon chip inside your Android phone has 10 billion transistors etched onto a piece of silicon the size of a fingernail. VLSI engineers at Qualcomm designed every transistor, every wire, every logic gate — using software tools to 'draw' at 5 nanometre scale.",
                "cool_fact": "A human hair is 80,000 nanometres wide. Modern chips have features just 3 nanometres wide."
            },
            {
                "app": "Jio 5G towers",
                "emoji": "📡",
                "what_they_built": "RF engineers at Jio designed the antenna arrays on those towers — calculating the exact shape, orientation, and spacing of antennas to cover Pune's 243 sq km with reliable 5G signal. They also designed the low-noise amplifiers that pick up your phone's signal from 2 km away.",
                "cool_fact": "Jio installed 1 lakh 5G base stations in India in 18 months — fastest 5G rollout in the world."
            },
            {
                "app": "Fastag / ETC toll systems",
                "emoji": "🚗",
                "what_they_built": "The RFID reader at every toll booth was designed by an embedded systems engineer. It sends a radio wave, your FASTag reflects it with your account number encoded, and the reader processes it in 150ms. The embedded code runs on a microcontroller the size of a ₹2 coin.",
                "cool_fact": "India has 800+ FASTag-enabled toll plazas processing 80 lakh vehicles per day."
            },
            {
                "app": "Your smartwatch / fitness band",
                "emoji": "⌚",
                "what_they_built": "The heart rate sensor, GPS receiver, accelerometer, bluetooth radio, and OLED screen — all designed by ECE engineers, all fitting on a PCB smaller than a ₹10 coin, all running on a battery for 7 days.",
                "cool_fact": "Fitbit's entire sensing system draws less power than a single LED."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Physics: electric circuits, Ohm's law, capacitors, inductors",
                "becomes_in_engineering": "Analog circuit design — designing the amplifiers, filters, and power circuits inside every electronic device",
                "emoji": "⚡"
            },
            {
                "knew_in_12th": "Physics: electromagnetic waves, light, optics",
                "becomes_in_engineering": "Communication systems and RF engineering — how signals travel through the air as waves and are received by antennas",
                "emoji": "📡"
            },
            {
                "knew_in_12th": "Maths: Fourier series, signals, differential equations",
                "becomes_in_engineering": "Digital Signal Processing — how to filter noise, compress audio/video, and extract information from sensor readings",
                "emoji": "〜"
            },
            {
                "knew_in_12th": "Computer Science / programming basics",
                "becomes_in_engineering": "Embedded C programming — writing firmware that runs directly on hardware with no operating system between your code and the chip",
                "emoji": "💾"
            },
        ],
        "real_problems": [
            {
                "problem": "An IoT sensor deployed in 10,000 farms was randomly rebooting every 2-3 days — making it useless for farmers who needed continuous soil moisture data.",
                "why_it_happened": "A slow memory leak in the firmware — the RAM gradually filled up until the microcontroller crashed and restarted.",
                "how_engineers_fixed_it": "The ECE engineer added heap memory monitoring that logged usage every hour to flash memory. After 48 hours, the log showed RAM growing by 200 bytes per hour. Found the bug: a buffer that was allocated but never freed in the sensor reading loop. Fixed in 20 minutes.",
                "lesson": "In embedded systems, you debug with oscilloscopes and log files, not IDE debuggers. The skill is systematically instrumenting your code.",
                "emoji": "🌱"
            },
            {
                "problem": "A PCB that passed all tests in the lab mysteriously failed 30% of the time in the field — but only near kitchen appliances.",
                "why_it_happened": "Microwave ovens emit strong electromagnetic interference at 2.45 GHz — exactly where the PCB's Wi-Fi module operated. The PCB had no RF shielding.",
                "how_engineers_fixed_it": "Added a metal shield can over the Wi-Fi module on the PCB. Redesigned the ground plane for better EMI isolation. Added software-side channel hopping. Field failure rate dropped from 30% to 0.1%.",
                "lesson": "Real-world electronics engineering involves electromagnetic compatibility (EMC) — making sure your device works in the same room as other devices.",
                "emoji": "🔌"
            },
            {
                "problem": "A new chip design failed to boot correctly 15% of the time after production — costing the company ₹50 crore in defective chips.",
                "why_it_happened": "The 1.8V power rail had voltage spikes during startup. The chip's internal logic was seeing incorrect voltage levels and misreading initial values.",
                "how_engineers_fixed_it": "VLSI engineers added decoupling capacitors closer to the power pins in a PCB redesign, and added a soft-start circuit to slow the power ramp rate. Boot failure rate dropped to 0.001%.",
                "lesson": "Power integrity is one of the most critical and underappreciated skills in hardware design.",
                "emoji": "⚙️"
            },
        ],
        "personality_fit": [
            "You've opened up a broken device to see what's inside — and weren't satisfied until you understood at least one component",
            "Physics circuits chapter was actually interesting to you — not just something to memorise",
            "You're drawn to things that work at the boundary of hardware and software",
            "You find it satisfying to make something physically work — LEDs blinking, motors turning, sensors reading",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Scope out the power rail", "detail": "The IoT board is randomly rebooting. Plug in the oscilloscope and capture the 3.3V rail. There it is — a 400mV spike every time the WiFi transmits.", "mood": "detective"},
            {"time": "10:00 AM", "task": "PCB redesign", "detail": "Open KiCAD. Move the decoupling capacitors closer to the WiFi chip's power pins. Add a larger bulk capacitor. Update the PCB layout.", "mood": "focus"},
            {"time": "11:30 AM", "task": "Write embedded firmware", "detail": "Implement the power-save mode in C — put the sensor to sleep between readings. Target: battery life from 6 months to 18 months.", "mood": "creative"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "The lab smells like solder and coffee. Hardware engineers often eat together — good place to ask 'has anyone dealt with this before?'", "mood": "break"},
            {"time": "2:00 PM", "task": "Test firmware on dev board", "detail": "Flash the new code, measure sleep current with a precision ammeter. 8 microamps. Perfect — matches the target. Document the measurement.", "mood": "win"},
            {"time": "3:30 PM", "task": "Design review meeting", "detail": "Present the power rail fix and battery life improvement to the team. Someone asks about the antenna placement — that's tomorrow's problem.", "mood": "team"},
            {"time": "5:00 PM", "task": "Send Gerbers to PCB manufacturer", "detail": "Export the PCB design files. 3-day lead time for prototype boards. You'll test the fix when they arrive.", "mood": "focus"},
        ],
        "tools": ["KiCAD / Altium (PCB design)", "Oscilloscope + Multimeter + Logic Analyser", "Keil / STM32CubeIDE (embedded firmware)", "Xilinx Vivado (FPGA / Verilog)", "LTSpice / Proteus (circuit simulation)", "Python / MATLAB (signal analysis)"],
        "reality_check": "Hardware bugs can take days to find. A software bug is fixed by editing a file; a hardware bug means redesigning and manufacturing a new board — which takes days and costs money. This is why ECE engineers are extremely methodical. The best ECE engineers think in hardware AND software simultaneously — that combination is rare and extremely well-paid.",
        "salary_snapshot": "Fresher at embedded/VLSI company: ₹5–10 LPA. Senior VLSI engineer at Qualcomm/Intel after 7 years: ₹30–70 LPA.",
        "youtube_search": "day in the life electronics embedded engineer",
        
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Scenario bank (unchanged — keep all 4×4 scenarios)
# ─────────────────────────────────────────────────────────────────────────────

SCENARIOS: Dict[str, List[Dict]] = {

    # ── CSE — everyday app/logic situations, no jargon ──────────────────────
    "CSE": [
        {
            "id": 1,
            "title": "📱  Your app crashes when too many people use it",
            "context": (
                "You built a food-ordering app for your college. It works perfectly "
                "when 5 people test it. But on the first day of the college fest, "
                "200 people open the app simultaneously — and it stops responding for everyone."
            ),
            "situation": "What is the MOST LIKELY reason this happened?",
            "options": [
                {
                    "id": "A",
                    "text": "The app has a typo in the code",
                    "score": 1,
                    "feedback": "❌ A typo would have broken the app even for 1 person.",
                    "explanation": "Typos are consistent bugs — they break the app for everyone all the time. "
                                   "This worked fine for 5 people but broke for 200, which tells you the issue is about load (scale), not a logic error."
                },
                {
                    "id": "B",
                    "text": "The server ran out of resources — memory or database connections got exhausted",
                    "score": 10,
                    "feedback": "✅ Exactly right. This is called a 'scalability problem' — the most common real-world software failure.",
                    "explanation": "Every server has a limit on how many requests it can handle at once. "
                                   "200 simultaneous users hit that limit. Engineers fix this by optimising resource usage, "
                                   "adding more servers, or using a waiting queue. This is what 'system design' is about."
                },
                {
                    "id": "C",
                    "text": "Someone hacked the app and took it down",
                    "score": 2,
                    "feedback": "Unlikely in this scenario — the timing matches a load spike, not an attack.",
                    "explanation": "While hacking is possible, a crash that happens exactly when 200 people join simultaneously "
                                   "is almost always a resource exhaustion problem, not an attack."
                }
            ],
            "learning": "Software that works for 5 people often breaks for 5000. Engineers must design for scale — this is one of the most important skills in software development."
        },
        {
            "id": 2,
            "title": "🐛  A bug that only one user can see",
            "context": (
                "A user messages you: 'Every time I log in, I see someone else's order history.' "
                "You try it yourself and everything looks normal. Your test accounts work perfectly."
            ),
            "situation": "This is a serious bug — some users are seeing other users' private data. How do you approach it?",
            "options": [
                {
                    "id": "A",
                    "text": "Reply to the user saying it works fine on your end, so it must be their device",
                    "score": 0,
                    "feedback": "❌ Never dismiss a bug just because you can't reproduce it — especially one involving private data.",
                    "explanation": "The user is seeing real data that belongs to someone else. That is a serious privacy breach. "
                                   "Dismissing it means it will keep happening. Real engineers take every report seriously."
                },
                {
                    "id": "B",
                    "text": "Check the code that fetches order history — look for where it identifies 'which user' to load data for",
                    "score": 10,
                    "feedback": "✅ Perfect instinct. The bug is in the logic that connects a user to their data.",
                    "explanation": "This is called an 'authorisation bug' — the system is loading data for the wrong user. "
                                   "By looking at the code that fetches the data, you'll find where user IDs are being mixed up. "
                                   "This is one of the most important security problems in web applications."
                },
                {
                    "id": "C",
                    "text": "Take the app offline immediately and put up a maintenance notice",
                    "score": 6,
                    "feedback": "Taking it offline is responsible — but you also need to find and fix the root cause.",
                    "explanation": "Taking down the app protects users while you investigate, which is reasonable. "
                                   "But the real answer is B — taking it down AND fixing the bug. "
                                   "Taking it down alone without understanding the cause doesn't solve anything."
                }
            ],
            "learning": "When users report strange behaviour with their data, it's almost always an authorisation bug — the code is accidentally showing one person's data to another. These must always be investigated seriously."
        },
        {
            "id": 3,
            "title": "🤝  Two people edited the same file",
            "context": (
                "You and your project partner are both working on the same Python file for your college project. "
                "You both made changes yesterday. Today, when your partner uploaded their version, "
                "all your changes disappeared. You have to redo 3 hours of work."
            ),
            "situation": "How do you prevent this from ever happening again?",
            "options": [
                {
                    "id": "A",
                    "text": "Only one person works on the project at a time — take turns",
                    "score": 4,
                    "feedback": "This works but completely kills your productivity. Real teams have 50+ people working simultaneously.",
                    "explanation": "Waiting for your turn would make software development impossibly slow. "
                                   "There's a much better solution that all professional developers use."
                },
                {
                    "id": "B",
                    "text": "Use Git — version control software where every change is tracked and conflicts are highlighted and merged",
                    "score": 10,
                    "feedback": "✅ This is exactly what Git was built for — and it's used by every software team on Earth.",
                    "explanation": "Git tracks every change made by every person. When two people edit the same file, "
                                   "Git highlights the conflict and lets you choose which changes to keep. "
                                   "Learning Git is one of the first things you do in a CSE job. It's non-negotiable."
                },
                {
                    "id": "C",
                    "text": "Keep a backup copy of every file every hour — just restore from backup if something is overwritten",
                    "score": 3,
                    "feedback": "Backups help with recovery but don't prevent the conflict in the first place.",
                    "explanation": "Backups help if you lose work, but they don't tell you whose changes to keep "
                                   "or help you merge two people's edits intelligently. Git solves all of this."
                }
            ],
            "learning": "Version control (Git) is the foundational tool of every software team. It tracks every change, every person, every version. Learning it is one of the first things you do as a developer."
        },
        {
            "id": 4,
            "title": "🔔  Notification sent 3 times",
            "context": (
                "Users of your app are complaining that they received the same birthday wish notification "
                "3 times in a row. You check the code — it looks correct. "
                "The notification function is called once. Yet users got it 3 times."
            ),
            "situation": "What type of bug most likely caused this?",
            "options": [
                {
                    "id": "A",
                    "text": "There is a typo in the notification message",
                    "score": 0,
                    "feedback": "❌ A typo would change the message text, not send it multiple times.",
                    "explanation": "Typos affect content, not how many times something runs. "
                                   "The issue here is about execution count, not the message itself."
                },
                {
                    "id": "B",
                    "text": "The function that sends notifications ran 3 times — there are probably 3 places in the code that call it",
                    "score": 9,
                    "feedback": "✅ Very likely — duplicate code paths is the most common cause of 'sent multiple times' bugs.",
                    "explanation": "If three different parts of your code all trigger the notification function, "
                                   "it runs three times. Engineers fix this by searching for all the places the function is called "
                                   "and making sure it's only triggered once per birthday."
                },
                {
                    "id": "C",
                    "text": "The notification system retried automatically because it thought the first one failed",
                    "score": 8,
                    "feedback": "✅ Also a very real cause — automatic retries without a 'already sent' check.",
                    "explanation": "Many notification systems automatically retry if they don't get a success confirmation. "
                                   "If the first notification sent successfully but the confirmation was lost, "
                                   "the system retries and sends again. Engineers fix this with 'idempotency' — "
                                   "making sure sending twice has no effect after the first send."
                }
            ],
            "learning": "When something runs more than once unexpectedly, look for either duplicate code calling the same function, or a retry system without a 'already done' check. Both are extremely common in real apps."
        }
    ],

    # ── CSE-AIML — everyday AI/data logic, no ML terminology ────────────────
    "CSE-AIML": [
        {
            "id": 1,
            "title": "🎵  Music app recommends only one genre",
            "context": (
                "You built a music recommendation feature for a college app. "
                "The app recommends songs based on what students have listened to before. "
                "But every student — whether they like classical, rock, or jazz — "
                "keeps getting recommended only Bollywood songs."
            ),
            "situation": "What went wrong with the AI recommendation system?",
            "options": [
                {
                    "id": "A",
                    "text": "The algorithm is too simple — replace it with a more complex one",
                    "score": 3,
                    "feedback": "Complexity is not the problem here — bad training data is.",
                    "explanation": "Making the algorithm more complex won't fix the issue if the data it learned from is unbalanced. "
                                   "You'd end up with a more complex system that still recommends only Bollywood."
                },
                {
                    "id": "B",
                    "text": "The training data had too many Bollywood songs — the AI learned that everyone likes Bollywood",
                    "score": 10,
                    "feedback": "✅ Exactly. Garbage in, garbage out — this is the most fundamental rule of AI.",
                    "explanation": "If 90% of your training songs are Bollywood, the AI concludes that Bollywood = good music. "
                                   "It has no evidence that anyone likes anything else. "
                                   "The fix is balanced training data — equal representation of all genres, "
                                   "and using each user's actual listening history to personalise."
                },
                {
                    "id": "C",
                    "text": "Bollywood is the most popular genre, so the AI is technically correct",
                    "score": 2,
                    "feedback": "Popularity doesn't equal personalisation — recommendation systems should be personal, not generic.",
                    "explanation": "A recommendation that tells everyone 'listen to the most popular thing' is not a recommendation — "
                                   "it's just a chart. The whole point of AI recommendations is to find what THIS specific user will enjoy."
                }
            ],
            "learning": "The quality of an AI model is determined entirely by the quality of the data it learned from. If the training data is biased or unbalanced, the AI will be too — regardless of how sophisticated the algorithm is."
        },
        {
            "id": 2,
            "title": "🌿  Plant disease app fails for poor farmers",
            "context": (
                "You trained an AI to detect plant diseases from photos. It works great in testing — "
                "98% accuracy. But after launching, farmers in rural Maharashtra say the app "
                "keeps saying 'plant is healthy' even when the crop is visibly sick."
            ),
            "situation": "What is the most likely reason the app fails for these farmers specifically?",
            "options": [
                {
                    "id": "A",
                    "text": "Rural farmers don't know how to use the app correctly",
                    "score": 0,
                    "feedback": "❌ Blaming users is never the answer. The engineer's job is to make the app work for all users.",
                    "explanation": "If the app only works for tech-savvy users in controlled conditions, it has failed its purpose. "
                                   "An AI built to help farmers must work for farmers."
                },
                {
                    "id": "B",
                    "text": "The training photos were likely high-quality photos taken in good lighting — but farmers take blurry, low-light photos on cheap phones",
                    "score": 10,
                    "feedback": "✅ Exactly right. The AI learned from perfect photos but encounters real-world imperfect photos.",
                    "explanation": "If all training data was professional close-up photos in bright sunlight, "
                                   "the AI genuinely doesn't know what disease looks like in a blurry, low-light photo taken from 1 metre away. "
                                   "The fix: collect training photos from actual farmers using actual cheap phones in real conditions."
                },
                {
                    "id": "C",
                    "text": "The AI needs more computing power to work on rural internet connections",
                    "score": 3,
                    "feedback": "Internet speed affects how fast results load, not whether the AI detects disease correctly.",
                    "explanation": "The AI runs the photo through its model and gives a result. "
                                   "Slow internet makes this take longer but doesn't change the answer. "
                                   "The problem is with what the AI learned, not how fast it loads."
                }
            ],
            "learning": "AI systems fail when real-world conditions don't match training conditions. Always collect training data that represents the actual users and environments your AI will encounter — not just convenient lab conditions."
        },
        {
            "id": 3,
            "title": "🎓  AI marks attendance — but unfairly",
            "context": (
                "Your college installs an AI face recognition system to mark student attendance automatically. "
                "It works well overall — 94% accuracy. But students with darker skin tones "
                "are marked absent 3× more often even when they are present."
            ),
            "situation": "Your principal wants to use this system for exams where a wrong 'absent' mark could mean failing the semester. What do you recommend?",
            "options": [
                {
                    "id": "A",
                    "text": "Go ahead — 94% accuracy is impressive for an AI system",
                    "score": 1,
                    "feedback": "❌ 94% overall accuracy hides a serious fairness problem for specific students.",
                    "explanation": "Average accuracy is misleading when the errors are concentrated on one group. "
                                   "If the system fails 3× more for darker-skinned students, those students bear all the harm "
                                   "while others benefit. For high-stakes decisions like exams, this is unacceptable."
                },
                {
                    "id": "B",
                    "text": "Don't use it for high-stakes decisions until the fairness problem is fixed by collecting more diverse training photos",
                    "score": 10,
                    "feedback": "✅ Correct — fixing the training data imbalance is the right technical and ethical response.",
                    "explanation": "The system was likely trained on fewer photos of darker-skinned people, "
                                   "so it learned that feature less well. The fix is retraining with balanced representation. "
                                   "Never use a biased AI for decisions that affect people's futures."
                },
                {
                    "id": "C",
                    "text": "Use it but let affected students appeal if they are marked wrongly",
                    "score": 4,
                    "feedback": "Appeals are a partial fix but put the burden on the students who are already being discriminated against.",
                    "explanation": "Making specific groups prove they were present — while others are automatically believed — "
                                   "is an unfair process. The real fix is addressing the bias in the model, not creating a workaround."
                }
            ],
            "learning": "AI fairness is not just a technical issue — it has direct consequences for real people. Systems must be tested for fairness across all groups, not just overall accuracy, before being used for important decisions."
        },
        {
            "id": 4,
            "title": "📰  Fake news detector has a problem",
            "context": (
                "You train an AI to detect fake news. You test it and get 97% accuracy. "
                "Excited, you show it to your professor. She asks: "
                "'What if someone writes fake news in a style that copies a real newspaper?' "
                "You test this — and the AI says it's real news every time."
            ),
            "situation": "What does this reveal about your AI model?",
            "options": [
                {
                    "id": "A",
                    "text": "The model learned to detect writing style, not actual facts",
                    "score": 10,
                    "feedback": "✅ Exactly — the model took a shortcut. Style is easier to learn than truth.",
                    "explanation": "Instead of learning what makes information true or false, the model learned "
                                   "'professional newspaper style = real, informal style = fake'. "
                                   "This is called learning a 'spurious correlation'. Anyone who copies the style "
                                   "of a real newspaper can fool the model, even with completely false content."
                },
                {
                    "id": "B",
                    "text": "The model needs to be larger to catch this type of fake news",
                    "score": 2,
                    "feedback": "A larger model learning the wrong thing will just be more confidently wrong.",
                    "explanation": "If the model is learning the wrong feature (style instead of content truthfulness), "
                                   "more parameters won't help — it'll just learn that wrong feature more thoroughly."
                },
                {
                    "id": "C",
                    "text": "97% accuracy is too low — you need at least 99% to handle edge cases",
                    "score": 3,
                    "feedback": "Accuracy percentage doesn't reveal what the model actually learned — that's a deeper problem.",
                    "explanation": "A model can be 97% accurate on test data while failing completely on a specific type of input. "
                                   "This is why engineers test AI on deliberately adversarial examples, not just random samples."
                }
            ],
            "learning": "AI models often learn shortcuts — easy patterns that work on training data but fail in the real world. Always ask: 'What did the model actually learn?' Test it deliberately with tricky examples, not just random ones."
        }
    ],

    # ── MECH — everyday physical situations, no engineering jargon ──────────
    "MECH": [
        {
            "id": 1,
            "title": "🪑  Canteen chair leg keeps breaking",
            "context": (
                "The college canteen bought 50 new steel chairs 3 months ago. "
                "8 of them have a broken leg — always the same front-right leg, "
                "always at the spot where the leg meets the seat frame. "
                "The steel used is good quality. The weight limit was not exceeded."
            ),
            "situation": "What is the most likely engineering reason the same leg keeps breaking at the same spot?",
            "options": [
                {
                    "id": "A",
                    "text": "Students are sitting on the chairs incorrectly",
                    "score": 1,
                    "feedback": "❌ Blaming users is not an engineering answer. A good design must handle real-world use.",
                    "explanation": "People naturally lean, tilt, and shift on chairs. A proper design accounts for this. "
                                   "If the chair breaks from normal use, it's an engineering failure, not user error."
                },
                {
                    "id": "B",
                    "text": "The joint where the leg meets the frame is a stress concentration point — that exact spot experiences the highest force every time someone sits or stands",
                    "score": 10,
                    "feedback": "✅ Exactly right. Where two parts meet is almost always the weakest point.",
                    "explanation": "When you sit down, force travels through the frame and concentrates at the joint. "
                                   "If the joint has a sharp corner or a weak weld, that's where the metal will fatigue and crack over thousands of cycles. "
                                   "The fix: redesign the joint with a rounded corner (called a fillet) to distribute the stress over a larger area."
                },
                {
                    "id": "C",
                    "text": "The steel delivered was fake — not the grade ordered",
                    "score": 4,
                    "feedback": "Possible, but the systematic pattern (same leg, same spot) points to a design issue, not material fraud.",
                    "explanation": "If the steel was uniformly bad, legs would break randomly everywhere. "
                                   "The fact that it's always the same leg, same spot, tells you the design concentrates stress there."
                }
            ],
            "learning": "In mechanical engineering, failure almost always happens at joints, sharp corners, or transitions — places where stress concentrates. The most important skill is predicting these spots before the product is built."
        },
        {
            "id": 2,
            "title": "🥤  Water bottle cracks in summer",
            "context": (
                "Your startup designed a plastic water bottle. It passed all lab tests. "
                "But after selling 10,000 units, customers in Nagpur and Rajasthan are returning "
                "cracked bottles. Customers in Pune and Mumbai are happy. "
                "You check — Nagpur and Rajasthan regularly reach 48°C in summer. "
                "Your lab tests were done at 25°C."
            ),
            "situation": "What was the fundamental mistake in your design process?",
            "options": [
                {
                    "id": "A",
                    "text": "The plastic grade used was too cheap",
                    "score": 5,
                    "feedback": "Possibly — but you don't know yet because you never tested at high temperatures.",
                    "explanation": "The plastic might be fine or might need upgrading — but without high-temperature testing, "
                                   "you can't tell. The root cause is the missing test, not necessarily the material."
                },
                {
                    "id": "B",
                    "text": "The design was only tested at lab conditions, not at the worst-case temperature customers would actually experience",
                    "score": 10,
                    "feedback": "✅ This is the fundamental mistake — always design and test for worst-case real conditions.",
                    "explanation": "A product that sells across India must be tested at 48°C, 100% humidity, and direct sunlight — "
                                   "not just comfortable lab conditions. This principle is called 'design for worst case'. "
                                   "Every mechanical engineer learns this the hard way, or learns it properly."
                },
                {
                    "id": "C",
                    "text": "Put a warning label: 'Do not use in temperatures above 40°C'",
                    "score": 2,
                    "feedback": "That's not engineering — that's just warning people that your product doesn't work.",
                    "explanation": "Warning labels don't fix the product. The engineering solution is to design "
                                   "a bottle that works in the conditions it will actually be used in."
                }
            ],
            "learning": "Always design and test for the worst conditions your product will encounter in the real world — not just comfortable lab conditions. For an Indian product, that means 48°C summer heat, monsoon humidity, and rough handling."
        },
        {
            "id": 3,
            "title": "🚲  College bike rental — brakes wear out too fast",
            "context": (
                "Your college launches a bike-sharing service with 30 cycles. "
                "After 2 months, 18 bikes have worn-out brakes that need replacing. "
                "The brake pads were supposed to last 6 months. "
                "The bikes are used mostly on the college's sloped roads, "
                "and students frequently brake hard going downhill."
            ),
            "situation": "The brake pads are wearing out 3× faster than expected. What is the engineering explanation?",
            "options": [
                {
                    "id": "A",
                    "text": "Students are braking too hard — they need to be trained to brake gently",
                    "score": 2,
                    "feedback": "Students braking hard downhill is expected behaviour, not misuse. The design must handle this.",
                    "explanation": "If your product fails when used exactly as intended, it's the design that needs to change. "
                                   "Braking hard on slopes is completely normal bike usage."
                },
                {
                    "id": "B",
                    "text": "The brake pad specification was for flat-road use — downhill braking generates much more heat and friction, wearing pads faster",
                    "score": 10,
                    "feedback": "✅ Correct. The pads were specified for average use, not for the actual use pattern on your campus.",
                    "explanation": "Brake pad life depends heavily on how they are used. Downhill braking means constant sustained braking, "
                                   "generating heat that accelerates wear. The fix: specify heavier-duty pads rated for hilly terrain, "
                                   "or increase the maintenance schedule for these bikes. This is called 'use-case analysis'."
                },
                {
                    "id": "C",
                    "text": "The brake pads are counterfeit — contact the supplier",
                    "score": 4,
                    "feedback": "Possible, but the consistent pattern across 18 bikes suggests a usage mismatch, not a product defect.",
                    "explanation": "If 18 out of 30 bikes have the same issue, and all are on a hilly campus, "
                                   "usage pattern is the more likely explanation than all 18 bikes having fake parts."
                }
            ],
            "learning": "In mechanical engineering, understanding the actual use pattern is as important as the design itself. A product designed for average use will fail under heavy use. Engineers must analyse real-world usage, not just average-case usage."
        },
        {
            "id": 4,
            "title": "❄️  Air conditioner struggles in summer",
            "context": (
                "Your college installs new ACs rated to cool a room to 22°C. "
                "In January they work perfectly. In May (when outside temperature is 44°C), "
                "the same ACs can only cool the room to 28°C — 6 degrees short of the spec."
            ),
            "situation": "The AC company says 'the AC is working correctly'. Are they right, and what is really happening?",
            "options": [
                {
                    "id": "A",
                    "text": "The AC company is wrong — 28°C means the AC is faulty",
                    "score": 4,
                    "feedback": "They might actually be right — the AC could be working at full capacity, just against tougher conditions.",
                    "explanation": "Before blaming the AC, you need to understand the relationship between outside temperature and cooling capacity."
                },
                {
                    "id": "B",
                    "text": "The AC might be working correctly — cooling capacity depends on the temperature difference between inside and outside. At 44°C outside, maintaining 22°C requires far more power than at 25°C outside",
                    "score": 10,
                    "feedback": "✅ This is exactly right — cooling capacity is not a fixed number, it depends on conditions.",
                    "explanation": "An AC rated at 1.5 tons works harder and achieves less cooling when outside is 44°C vs 25°C. "
                                   "The engineering fix: specify the AC rating at the worst-case summer temperature, not at standard test conditions (which are typically 35°C outside). "
                                   "If the spec says 22°C at 35°C outside, it may legally be working correctly at 28°C when it's 44°C outside."
                },
                {
                    "id": "C",
                    "text": "The electricity supply is weaker in summer due to grid overload",
                    "score": 3,
                    "feedback": "Voltage fluctuation is a real issue but would affect all electrical equipment, not just cooling performance.",
                    "explanation": "While grid issues can reduce AC performance slightly, the primary explanation for 6°C shortfall "
                                   "is the thermodynamic relationship between indoor-outdoor temperature difference and cooling capacity."
                }
            ],
            "learning": "In thermodynamics (heat engineering), performance is never a fixed number — it always depends on operating conditions. Engineers must always specify ratings at worst-case conditions, not standard lab conditions."
        }
    ],

    # ── ECE — everyday electronics situations, no circuit theory jargon ─────
    "ECE": [
        {
            "id": 1,
            "title": "💡  Arduino LED blinks randomly at home",
            "context": (
                "For your school science exhibition, you built an Arduino circuit that blinks "
                "an LED exactly once per second. It worked perfectly at school. "
                "At home, the LED blinks randomly — sometimes fast, sometimes slow, sometimes not at all. "
                "You didn't change any code. You're using your phone charger as power supply instead "
                "of the school's lab bench power supply."
            ),
            "situation": "The code is identical. What is the most likely reason it behaves differently at home?",
            "options": [
                {
                    "id": "A",
                    "text": "The Arduino board got damaged when you transported it",
                    "score": 3,
                    "feedback": "Possible, but the timing symptom points to a more specific and common cause.",
                    "explanation": "If the board was physically damaged, it would likely fail completely or behave very erratically. "
                                   "Timing issues specifically suggest a power supply problem."
                },
                {
                    "id": "B",
                    "text": "Phone chargers deliver 'noisy' power — small voltage fluctuations that confuse the Arduino's internal clock",
                    "score": 10,
                    "feedback": "✅ This is one of the most common beginner electronics problems.",
                    "explanation": "Lab bench power supplies are very stable and clean. Cheap phone chargers have ripple — "
                                   "small fluctuations in voltage that happen at different rates. "
                                   "The Arduino uses power supply stability to count time accurately. "
                                   "Noisy power = inaccurate timing. Fix: add a small capacitor across the power pins "
                                   "to smooth out the ripple, or use a proper regulated power adapter."
                },
                {
                    "id": "C",
                    "text": "Your home WiFi is interfering with the Arduino's timing",
                    "score": 2,
                    "feedback": "WiFi doesn't typically affect a basic Arduino timing circuit.",
                    "explanation": "Unless your Arduino has a WiFi module and is using radio frequencies, "
                                   "household WiFi won't affect a simple LED blink program. Power supply is the much more likely cause."
                }
            ],
            "learning": "Power supply quality is one of the most underappreciated aspects of electronics. Cheap or noisy power supplies cause mysterious, hard-to-diagnose problems. Electronics engineers always check power quality first when behaviour is erratic."
        },
        {
            "id": 2,
            "title": "🔊  Speaker distorts at high volume",
            "context": (
                "You build a simple Bluetooth speaker for a college project. "
                "At low volume it sounds crystal clear. "
                "But when you turn it up to 70% volume, the sound becomes harsh, "
                "crackly, and distorted — like a cheap radio. "
                "The speaker itself is good quality."
            ),
            "situation": "What is most likely causing the distortion at high volume?",
            "options": [
                {
                    "id": "A",
                    "text": "The Bluetooth signal is getting corrupted",
                    "score": 2,
                    "feedback": "Bluetooth corruption would affect all volume levels equally, not just high volumes.",
                    "explanation": "Bluetooth transmits a digital signal — it either arrives correctly or it doesn't. "
                                   "A problem that only appears at high volume is an analog power problem, not a digital transmission problem."
                },
                {
                    "id": "B",
                    "text": "The amplifier chip is being pushed beyond its power limit — it's trying to produce more power than it can handle",
                    "score": 10,
                    "feedback": "✅ Exactly — this is called 'clipping', the most common cause of speaker distortion.",
                    "explanation": "Every amplifier has a maximum output power. Beyond that point, instead of making the sound louder, "
                                   "the tops and bottoms of the audio wave get cut off (clipped). "
                                   "This creates that harsh, crackling sound. Fix: use a more powerful amplifier chip, "
                                   "or limit the maximum volume in software."
                },
                {
                    "id": "C",
                    "text": "The speaker cone is too small for high volumes",
                    "score": 4,
                    "feedback": "Possible if the speaker is severely underpowered, but amplifier clipping is far more common.",
                    "explanation": "A speaker cone can produce distortion if it's physically moving beyond its limits, "
                                   "but this typically happens at very high volumes. The amplifier clipping usually happens first."
                }
            ],
            "learning": "In electronics, 'clipping' occurs when an amplifier is driven beyond its power rating. It's one of the most common audio problems and is fixed by matching the amplifier power rating to the required output — or limiting the input signal."
        },
        {
            "id": 3,
            "title": "🔋  Smartwatch battery dies in 1 day in summer",
            "context": (
                "You design a smartwatch that is advertised as having a 7-day battery life. "
                "Users in Pune and Delhi complain it lasts only 1 day in summer. "
                "Users in Shimla and Manali (hill stations) report the full 7 days. "
                "Nothing is different between the watches — same model, same software."
            ),
            "situation": "What is causing the battery to drain so much faster in hot places?",
            "options": [
                {
                    "id": "A",
                    "text": "People in hot cities use their phones more, so they check the watch more often",
                    "score": 2,
                    "feedback": "This doesn't explain a 7× difference in battery life.",
                    "explanation": "Even heavy usage wouldn't reduce battery from 7 days to 1 day. "
                                   "A physical effect of temperature is the more likely explanation."
                },
                {
                    "id": "B",
                    "text": "Heat makes lithium batteries less efficient — high temperatures cause the battery to discharge faster and also damage its capacity over time",
                    "score": 10,
                    "feedback": "✅ Correct. Temperature is the biggest enemy of lithium battery performance.",
                    "explanation": "Lithium batteries have an ideal operating range of 15°C–35°C. "
                                   "Above 35°C, internal resistance increases, self-discharge accelerates, and capacity drops. "
                                   "At 45°C ambient (which a wrist-worn device can reach easily in Pune summer), "
                                   "effective capacity can drop by 30–50%. Engineers must specify battery life at maximum operating temperature, not just room temperature."
                },
                {
                    "id": "C",
                    "text": "The display is brighter in sunlight due to auto-brightness, using more power",
                    "score": 5,
                    "feedback": "Auto-brightness does increase display power, but it explains hours, not a 7× difference.",
                    "explanation": "Display brightness increase from auto-brightness might add 20-30% drain. "
                                   "A 7× difference (7 days → 1 day) requires a more fundamental cause like battery chemistry being affected by temperature."
                }
            ],
            "learning": "Temperature is one of the most important factors in electronics design — especially for batteries. Engineers always specify and test device performance at the extremes of the operating temperature range, not just at room temperature."
        },
        {
            "id": 4,
            "title": "📡  Circuit works on desk but not inside a metal box",
            "context": (
                "You design a small wireless sensor circuit. On your desk it works perfectly — "
                "sends data every 5 seconds without fail. "
                "You put the circuit inside a metal enclosure (box) to protect it. "
                "Now it stops sending data completely. "
                "You open the box — it works again. Close it — stops again."
            ),
            "situation": "What is the metal box doing to your circuit?",
            "options": [
                {
                    "id": "A",
                    "text": "The metal box is getting hot and overheating the circuit",
                    "score": 3,
                    "feedback": "Heat could be a factor, but the immediate on/off behaviour with the box being opened/closed points to a different cause.",
                    "explanation": "If it were heat, there would be a delay — the temperature would need time to build up. "
                                   "The immediate failure when you close the box suggests something instantaneous."
                },
                {
                    "id": "B",
                    "text": "The metal box is acting as a Faraday cage — blocking the radio signals the circuit uses to send data",
                    "score": 10,
                    "feedback": "✅ Classic Faraday cage effect — every ECE student learns this.",
                    "explanation": "Metal enclosures block electromagnetic waves — including the radio waves your wireless sensor uses. "
                                   "This is called the Faraday cage effect. Fix: drill a small hole for an external antenna, "
                                   "or position the antenna to poke outside the box. "
                                   "This is why your microwave oven has a metal mesh on the door — it keeps microwaves inside."
                },
                {
                    "id": "C",
                    "text": "The metal box is too heavy and pressing down on the circuit board, damaging connections",
                    "score": 2,
                    "feedback": "If physical pressure caused damage, the circuit would stay broken after you open the box.",
                    "explanation": "Since the circuit works again as soon as you open the box, there's no permanent damage. "
                                   "The effect is immediate and reversible — which means the metal is affecting the signal propagation, not the physical connections."
                }
            ],
            "learning": "Metal enclosures block radio signals — a phenomenon called the Faraday cage effect. This is one of the first things ECE students learn in electromagnetic theory. Wireless sensors, GPS receivers, and any radio device must have their antenna outside or accessible through the enclosure."
        }
    ],
}

BRANCH_NAMES  = {"CSE": "Computer Science & Engineering", "CSE-AIML": "CSE with AI & Machine Learning",
                 "MECH": "Mechanical Engineering", "ECE": "Electronics & Communication Engineering"}
BRANCH_EMOJIS = {"CSE": "💻", "CSE-AIML": "🤖", "MECH": "⚙️", "ECE": "🔌"}


class DayInLifeSimulator:
    def get_available_branches(self): return list(SCENARIOS.keys())
    def get_branch_info(self, code):
        return {"code": code, "name": BRANCH_NAMES.get(code, code),
                "emoji": BRANCH_EMOJIS.get(code, "🎓"),
                "total_scenarios": len(SCENARIOS.get(code, []))}
    def get_intro(self, code): return BRANCH_INTRO.get(code.upper())
    def get_scenario(self, branch_code, scenario_index):
        scenarios = SCENARIOS.get(branch_code, [])
        if 0 <= scenario_index < len(scenarios):
            s = scenarios[scenario_index].copy()
            s["index"] = scenario_index; s["total"] = len(scenarios)
            s["branch_code"] = branch_code; s["branch_name"] = BRANCH_NAMES.get(branch_code, branch_code)
            return s
        return None
    def evaluate_choice(self, branch_code, scenario_index, choice_id):
        scenario = self.get_scenario(branch_code, scenario_index)
        if not scenario: return {"error": "Invalid scenario"}
        chosen = next((o for o in scenario["options"] if o["id"] == choice_id), None)
        if not chosen: return {"error": "Invalid choice"}
        is_last = (scenario_index + 1) >= scenario["total"]
        return {"choice_id": choice_id, "score": chosen["score"], "max_score": 10,
                "feedback": chosen["feedback"], "explanation": chosen["explanation"],
                "learning": scenario["learning"], "scenario_title": scenario["title"],
                "is_last": is_last, "next_index": scenario_index + 1 if not is_last else None}
    def calculate_final_score(self, decisions):
        if not decisions: return {"error": "No decisions"}
        total = sum(d.get("score", 0) for d in decisions)
        max_p = len(decisions) * 10
        pct   = round(total / max_p * 100, 1) if max_p else 0
        if   pct >= 85: level, msg, emoji = "Outstanding", "You think like a practising engineer! This branch suits you very well.", "🏆"
        elif pct >= 70: level, msg, emoji = "Good",         "Solid judgment. A bit of learning and you'd excel here.", "✅"
        elif pct >= 50: level, msg, emoji = "Developing",   "You have the right instincts — keep exploring this field.", "📈"
        else:           level, msg, emoji = "Needs Work",   "This field might need more study before it clicks. Try other branches too.", "💡"
        return {"total_score": total, "max_score": max_p, "percentage": pct,
                "level": level, "message": msg, "emoji": emoji, "decisions": len(decisions)}


if __name__ == "__main__":
    sim = DayInLifeSimulator()
    for code in sim.get_available_branches():
        intro = sim.get_intro(code)
        print(f"\n{BRANCH_EMOJIS[code]} {BRANCH_NAMES[code]}")
        print(f"  Tagline    : {intro['tagline'][:60]}...")
        print(f"  Real apps  : {len(intro['real_apps'])}")
        print(f"  Bridge 12th: {len(intro['bridge_12th'])}")
        print(f"  Problems   : {len(intro['real_problems'])}")
        print(f"  YT Search  : {intro['youtube_search']}")
    print("\n✅ Simulator OK")
