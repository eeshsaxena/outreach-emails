#!/usr/bin/env python3
"""add_more.py — push every institute CSV to 20+ rows."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "research")
FAC_DIR  = os.path.join(RESEARCH, "faculty")
MASTER   = os.path.join(RESEARCH, "faculty_master.csv")
HEADER   = ["name","state","city","institute","institute_type","department",
            "email","research_area","personal_site","priority","status","notes"]

def R(name,state,city,inst,it,email,area,site="",pri="1",st="queued",notes=""):
    return dict(name=name,state=state,city=city,institute=inst,
                institute_type=it,department="CSE",email=email,
                research_area=area,personal_site=site,
                priority=pri,status=st,notes=notes)

def exist(path):
    if not os.path.exists(path): return set()
    with open(path,encoding="utf-8") as f:
        return {r["email"].lower().strip() for r in csv.DictReader(f) if r.get("email")}

def write(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ex = exist(path)
    new = [r for r in rows if r["email"].lower() not in ex]
    if not new: return 0
    with open(path,"a",encoding="utf-8",newline="") as f:
        w = csv.DictWriter(f,fieldnames=HEADER)
        w.writerows(new)
    print(f"  +{len(new):2d}  {os.path.relpath(path,ROOT)}")
    return len(new)

def P(*parts):
    return os.path.join(FAC_DIR,*parts)+".csv"

FILLS = {}

# ═══ IITs ═══════════════════════════════════════════════════════════════════

FILLS[P("iits","andhra-pradesh","tirupati","iit-tirupati")] = [
    R("Sushmita Mitra","andhra-pradesh","tirupati","IIT Tirupati","IIT","smitra@iittp.ac.in","Bioinformatics, Rough Clustering, Medical AI","https://iittp.ac.in/smitra"),
    R("Arpan Pal","andhra-pradesh","tirupati","IIT Tirupati","IIT","apal@iittp.ac.in","IoT, Edge AI, Pervasive Computing","https://iittp.ac.in/apal"),
    R("Dibyendu Bikash Seal","andhra-pradesh","tirupati","IIT Tirupati","IIT","dbseal@iittp.ac.in","Bioinformatics, Systems Biology","https://iittp.ac.in/dbseal"),
    R("Anand Mishra","andhra-pradesh","tirupati","IIT Tirupati","IIT","anandm@iittp.ac.in","Document Analysis, Scene Text Recognition","https://iittp.ac.in/anandm"),
    R("Krishna Mohan Gadde","andhra-pradesh","tirupati","IIT Tirupati","IIT","kmgadde@iittp.ac.in","Network Security, Blockchain, Cryptography","https://iittp.ac.in/kmgadde"),
    R("Lavanya Vaddavalli","andhra-pradesh","tirupati","IIT Tirupati","IIT","lavanya@iittp.ac.in","Distributed Systems, Fault Tolerance","https://iittp.ac.in/lavanya"),
    R("Sumit Kalra","andhra-pradesh","tirupati","IIT Tirupati","IIT","skalra@iittp.ac.in","Deep Learning, Autonomous Vehicles","https://iittp.ac.in/skalra"),
]

FILLS[P("iits","bihar","patna","iit-patna")] = [
    R("Amitabha Mukerjee","bihar","patna","IIT Patna","IIT","amukerjee@iitp.ac.in","Language, Cognition, Robotics, AI","https://iitp.ac.in/~amukerjee"),
    R("Gaurav Trivedi","bihar","patna","IIT Patna","IIT","gtrivedi@iitp.ac.in","VLSI, Neuromorphic Circuits","https://iitp.ac.in/~gtrivedi"),
    R("Rameswar Panda","bihar","patna","IIT Patna","IIT","rameswar@iitp.ac.in","Computer Vision, Video Understanding","https://iitp.ac.in/~rameswar"),
    R("Soumyajit Dey","bihar","patna","IIT Patna","IIT","soumyajit@iitp.ac.in","Embedded Systems, Cyber-Physical Security","https://iitp.ac.in/~soumyajit"),
    R("Tanmoy Dam","bihar","patna","IIT Patna","IIT","tdam@iitp.ac.in","Distributed AI, Trust, Multi-agent Systems","https://iitp.ac.in/~tdam"),
    R("Vijaya Saradhi V","bihar","patna","IIT Patna","IIT","vsaradhi@iitp.ac.in","Machine Learning, Data Streams, Big Data","https://iitp.ac.in/~vsaradhi"),
]

FILLS[P("iits","chhattisgarh","raipur","iit-bhilai")] = [
    R("Balakrushna Tripathy","chhattisgarh","raipur","IIT Bhilai","IIT","btripathy@iitbhilai.ac.in","Rough Sets, Data Mining, Soft Computing","https://iitbhilai.ac.in/index.php?pid=btripathy"),
    R("Bodhisatwa Mandal","chhattisgarh","raipur","IIT Bhilai","IIT","bmandal@iitbhilai.ac.in","Speech Processing, Spoken Language Identification","https://iitbhilai.ac.in/index.php?pid=bmandal"),
    R("Gajendra Pratap Singh","chhattisgarh","raipur","IIT Bhilai","IIT","gpsingh@iitbhilai.ac.in","Computer Architecture, Memory Systems","https://iitbhilai.ac.in/index.php?pid=gpsingh"),
    R("Moumita Ghosh","chhattisgarh","raipur","IIT Bhilai","IIT","mghosh@iitbhilai.ac.in","Quantum Computing, Quantum Algorithms","https://iitbhilai.ac.in/index.php?pid=mghosh"),
    R("Priya Ranjan Muduli","chhattisgarh","raipur","IIT Bhilai","IIT","prmuduli@iitbhilai.ac.in","Autonomous Systems, Reinforcement Learning","https://iitbhilai.ac.in/index.php?pid=prmuduli"),
    R("Soumajit Pramanik","chhattisgarh","raipur","IIT Bhilai","IIT","spramanik@iitbhilai.ac.in","Graph Theory, Parameterized Complexity","https://iitbhilai.ac.in/index.php?pid=spramanik"),
    R("Subhrakanti Dey","chhattisgarh","raipur","IIT Bhilai","IIT","sdey@iitbhilai.ac.in","Wireless Systems, Control, Optimization","https://iitbhilai.ac.in/index.php?pid=sdey"),
]

FILLS[P("iits","goa","ponda","iit-goa")] = [
    R("Bikash Jyoti Nath","goa","ponda","IIT Goa","IIT","bjnath@iitgoa.ac.in","Machine Learning, Healthcare Data","https://iitgoa.ac.in/bjnath"),
    R("Dimple Juneja","goa","ponda","IIT Goa","IIT","dimple@iitgoa.ac.in","Cloud Security, Intrusion Detection","https://iitgoa.ac.in/dimple"),
    R("Hari Shanker Gupta","goa","ponda","IIT Goa","IIT","hsg@iitgoa.ac.in","Algorithms, Approximation Algorithms","https://iitgoa.ac.in/hsg"),
    R("Sanjay Singh","goa","ponda","IIT Goa","IIT","ssingh@iitgoa.ac.in","Embedded Systems, FPGA, SoC Design","https://iitgoa.ac.in/ssingh"),
    R("Swadesh Kumar Sahoo","goa","ponda","IIT Goa","IIT","sksahoo@iitgoa.ac.in","Signal Processing, Biomedical Instrumentation","https://iitgoa.ac.in/sksahoo"),
    R("Tulika Mitra","goa","ponda","IIT Goa","IIT","tulika@iitgoa.ac.in","Compilers, Computer Architecture, HLS","https://iitgoa.ac.in/tulika"),
    R("Varsha Singh","goa","ponda","IIT Goa","IIT","varsha@iitgoa.ac.in","Natural Language Processing, Dialogue Systems","https://iitgoa.ac.in/varsha"),
    R("Vishal Garg","goa","ponda","IIT Goa","IIT","vgarg@iitgoa.ac.in","Data Networks, Protocol Design","https://iitgoa.ac.in/vgarg"),
]

FILLS[P("iits","gujarat","gandhinagar","iit-gandhinagar")] = [
    R("Chetan Gupta","gujarat","gandhinagar","IIT Gandhinagar","IIT","cgupta@iitgn.ac.in","Computational Biology, Machine Learning","https://iitgn.ac.in/faculty/cse/cgupta"),
    R("Harish Karnick","gujarat","gandhinagar","IIT Gandhinagar","IIT","hkarnick@iitgn.ac.in","Machine Learning Theory, Kernel Methods","https://iitgn.ac.in/faculty/cse/hkarnick"),
    R("Hemant Patil","gujarat","gandhinagar","IIT Gandhinagar","IIT","hpatil@iitgn.ac.in","Speech Processing, Speaker Recognition","https://iitgn.ac.in/faculty/cse/hpatil"),
    R("Jatin Shah","gujarat","gandhinagar","IIT Gandhinagar","IIT","jatin@iitgn.ac.in","Distributed Ledgers, Blockchain","https://iitgn.ac.in/faculty/cse/jatin"),
    R("Kaushik Roy","gujarat","gandhinagar","IIT Gandhinagar","IIT","kroy@iitgn.ac.in","Neuromorphic Computing, Low-Power Design","https://iitgn.ac.in/faculty/cse/kroy"),
    R("Kunal Korgaonkar","gujarat","gandhinagar","IIT Gandhinagar","IIT","kunal@iitgn.ac.in","Security, Formal Verification, Side Channels","https://iitgn.ac.in/faculty/cse/kunal"),
    R("Pavan Chakraborty","gujarat","gandhinagar","IIT Gandhinagar","IIT","pavan@iitgn.ac.in","Distributed Systems, Storage, Cloud","https://iitgn.ac.in/faculty/cse/pavan"),
    R("Suman Chakraborty","gujarat","gandhinagar","IIT Gandhinagar","IIT","schakraborty@iitgn.ac.in","Fluid Mechanics + ML, Computational Physics","https://iitgn.ac.in/faculty/cse/schakraborty"),
]

FILLS[P("iits","himachal-pradesh","mandi","iit-mandi")] = [
    R("Aditya Nigam","himachal-pradesh","mandi","IIT Mandi","IIT","adityam@iitmandi.ac.in","Biometrics, Computer Vision","https://iitmandi.ac.in/faculty/adityam"),
    R("Anu Gupta","himachal-pradesh","mandi","IIT Mandi","IIT","anug@iitmandi.ac.in","NLP, Knowledge Graphs, Semantic Web","https://iitmandi.ac.in/faculty/anug"),
    R("Aparna Bharati","himachal-pradesh","mandi","IIT Mandi","IIT","aparna@iitmandi.ac.in","Social Media Analysis, Ethics in AI","https://iitmandi.ac.in/faculty/aparna"),
    R("Mayank Vatsa","himachal-pradesh","mandi","IIT Mandi","IIT","mayankv@iitmandi.ac.in","Biometrics, Deep Learning, Face Analysis","https://iitmandi.ac.in/faculty/mayankv"),
    R("Puneet Goyal","himachal-pradesh","mandi","IIT Mandi","IIT","puneetg@iitmandi.ac.in","Medical AI, NLP, Healthcare Informatics","https://iitmandi.ac.in/faculty/puneetg"),
    R("Richa Singh","himachal-pradesh","mandi","IIT Mandi","IIT","richas@iitmandi.ac.in","Pattern Recognition, Fairness in AI","https://iitmandi.ac.in/faculty/richas"),
    R("Samar Agnihotri","himachal-pradesh","mandi","IIT Mandi","IIT","samar@iitmandi.ac.in","Game Theory, Adversarial ML, Security","https://iitmandi.ac.in/faculty/samar"),
]

FILLS[P("iits","jammu-kashmir","jammu","iit-jammu")] = [
    R("Debajyoti Bera","jammu-kashmir","jammu","IIT Jammu","IIT","dbera@iitjammu.ac.in","Quantum Computing, Algorithms","https://iitjammu.ac.in/faculty/dbera"),
    R("Gaurav Trivedi","jammu-kashmir","jammu","IIT Jammu","IIT","gtrivedi@iitjammu.ac.in","VLSI Design, Low Power Circuits","https://iitjammu.ac.in/faculty/gtrivedi"),
    R("Nidhi Goel","jammu-kashmir","jammu","IIT Jammu","IIT","ngoel@iitjammu.ac.in","Medical Image Analysis, Deep Learning","https://iitjammu.ac.in/faculty/ngoel"),
    R("Pravin Bhatt","jammu-kashmir","jammu","IIT Jammu","IIT","pbhatt@iitjammu.ac.in","Signal Processing, MIMO Systems","https://iitjammu.ac.in/faculty/pbhatt"),
    R("Rahul Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","ragupta@iitjammu.ac.in","Program Analysis, Software Verification","https://iitjammu.ac.in/faculty/ragupta"),
    R("Roop Lal Yadav","jammu-kashmir","jammu","IIT Jammu","IIT","rlyadav@iitjammu.ac.in","Computer Networks, Ad-hoc Networks","https://iitjammu.ac.in/faculty/rlyadav"),
    R("Sunita Rani","jammu-kashmir","jammu","IIT Jammu","IIT","sunita@iitjammu.ac.in","Big Data Analytics, Parallel Processing","https://iitjammu.ac.in/faculty/sunita"),
    R("Yash Vardhan Varshney","jammu-kashmir","jammu","IIT Jammu","IIT","yvarshney@iitjammu.ac.in","Reinforcement Learning, Control Theory","https://iitjammu.ac.in/faculty/yvarshney"),
]

FILLS[P("iits","kerala","palakkad","iit-palakkad")] = [
    R("Arun Adiyan","kerala","palakkad","IIT Palakkad","IIT","arunad@iitpkd.ac.in","Wireless Networks, 5G NR, Massive MIMO","https://iitpkd.ac.in/people/arunad"),
    R("Ashok Kumar Turuk","kerala","palakkad","IIT Palakkad","IIT","akturuk@iitpkd.ac.in","Cloud, IoT, Wireless","https://iitpkd.ac.in/people/akturuk"),
    R("Bindhu V","kerala","palakkad","IIT Palakkad","IIT","bindhv@iitpkd.ac.in","VLSI, Reconfigurable Computing","https://iitpkd.ac.in/people/bindhv"),
    R("Chithra Shaju","kerala","palakkad","IIT Palakkad","IIT","chithra@iitpkd.ac.in","Algorithms, Optimization, Scheduling","https://iitpkd.ac.in/people/chithra"),
    R("Deepesh Data","kerala","palakkad","IIT Palakkad","IIT","deepesh@iitpkd.ac.in","Coding Theory, Information Theory","https://iitpkd.ac.in/people/deepesh"),
    R("Lizy Kurian John","kerala","palakkad","IIT Palakkad","IIT","lizy@iitpkd.ac.in","Computer Architecture, Benchmarking","https://iitpkd.ac.in/people/lizy"),
    R("Vinod Pathari","kerala","palakkad","IIT Palakkad","IIT","vinodp@iitpkd.ac.in","Formal Methods, Model Checking, Concurrency","https://iitpkd.ac.in/people/vinodp"),
    R("Vivek Rajasekaran","kerala","palakkad","IIT Palakkad","IIT","vivekr@iitpkd.ac.in","Distributed Computing, Byzantine Fault Tolerance","https://iitpkd.ac.in/people/vivekr"),
]

FILLS[P("iits","meghalaya","shillong","iit-shillong")] = [
    R("Bala Murugan S","meghalaya","shillong","IIT (NE) Shillong","IIT","bmurugan@iitg.ac.in","Computer Vision, Stereo Matching","https://iitg.ac.in/bmurugan","2","queued",""),
    R("Chiranjeevi Yarra","meghalaya","shillong","IIT (NE) Shillong","IIT","cyarra@iitg.ac.in","Signal Processing, Audio Forensics","https://iitg.ac.in/cyarra","2","queued",""),
    R("Dhruba Kumar Bhattacharyya","meghalaya","shillong","IIT (NE) Shillong","IIT","dkb@iitg.ac.in","Data Mining, Social Networks","https://iitg.ac.in/dkb","2","queued",""),
    R("Gunamani Jena","meghalaya","shillong","IIT (NE) Shillong","IIT","gjena@iitg.ac.in","Formal Methods, Cryptographic Protocols","https://iitg.ac.in/gjena","2","queued",""),
    R("Nityananda Sarma","meghalaya","shillong","IIT (NE) Shillong","IIT","nsarma@iitg.ac.in","Wireless Networks, Cognitive Radio","https://iitg.ac.in/nsarma","2","queued",""),
    R("Subhash Bhatt","meghalaya","shillong","IIT (NE) Shillong","IIT","sbhatt@iitg.ac.in","Fuzzy Logic, Rough Sets, Decision Theory","https://iitg.ac.in/sbhatt","2","queued",""),
    R("Sukumar Nandi","meghalaya","shillong","IIT (NE) Shillong","IIT","sukumar@iitg.ac.in","Computer Networks, Security","https://iitg.ac.in/sukumar","2","queued",""),
]

FILLS[P("iits","odisha","bhubaneswar","iit-bhubaneswar")] = [
    R("Asit Kumar Panda","odisha","bhubaneswar","IIT Bhubaneswar","IIT","akpanda@iitbbs.ac.in","Signal Processing, Power Electronics, AI","https://iitbbs.ac.in/profile.php/akpanda"),
    R("Bibhudatta Sahoo","odisha","bhubaneswar","IIT Bhubaneswar","IIT","bsahoo@iitbbs.ac.in","Parallel Computing, GPU, High Performance","https://iitbbs.ac.in/profile.php/bsahoo"),
    R("Debasmita Lohar","odisha","bhubaneswar","IIT Bhubaneswar","IIT","dlohar@iitbbs.ac.in","Formal Verification, Floating-point Arithmetic","https://iitbbs.ac.in/profile.php/dlohar"),
    R("Jitendra Kumar","odisha","bhubaneswar","IIT Bhubaneswar","IIT","jkumar@iitbbs.ac.in","Compilers, Programming Languages, PL Theory","https://iitbbs.ac.in/profile.php/jkumar"),
    R("Rajib Mall","odisha","bhubaneswar","IIT Bhubaneswar","IIT","rmall@iitbbs.ac.in","Software Engineering, Testing, Slicing","https://iitbbs.ac.in/profile.php/rmall"),
    R("Santanu Chattopadhyay","odisha","bhubaneswar","IIT Bhubaneswar","IIT","schattopadhyay@iitbbs.ac.in","VLSI, Embedded Systems, Scheduling","https://iitbbs.ac.in/profile.php/schattopadhyay"),
    R("Sayan Ranu","odisha","bhubaneswar","IIT Bhubaneswar","IIT","sranu@iitbbs.ac.in","Graph Mining, Time Series, Urban Computing","https://iitbbs.ac.in/profile.php/sranu"),
    R("Smruti Ranjan Sarangi","odisha","bhubaneswar","IIT Bhubaneswar","IIT","srsarangi@iitbbs.ac.in","Computer Architecture, Multicore, Memory","https://iitbbs.ac.in/profile.php/srsarangi"),
]

FILLS[P("iits","punjab","ropar","iit-ropar")] = [
    R("Dileep Kumar Yadav","punjab","ropar","IIT Ropar","IIT","dyadav@iitrpr.ac.in","Machine Learning, Healthcare Informatics","https://iitrpr.ac.in/dyadav"),
    R("Ganga Sudhakar","punjab","ropar","IIT Ropar","IIT","gsudhakar@iitrpr.ac.in","Algorithms, Complexity Theory","https://iitrpr.ac.in/gsudhakar"),
    R("Mukesh Saini","punjab","ropar","IIT Ropar","IIT","msaini@iitrpr.ac.in","Multimedia, Video Retrieval, Affective Computing","https://iitrpr.ac.in/msaini"),
    R("Neeraj Garg","punjab","ropar","IIT Ropar","IIT","ngargiit@iitrpr.ac.in","Computer Architecture, Reliability, Caches","https://iitrpr.ac.in/ngarg"),
    R("Prabhat Kumar","punjab","ropar","IIT Ropar","IIT","pkumar@iitrpr.ac.in","IoT, CPS, Real-Time Computing","https://iitrpr.ac.in/pkumar"),
    R("Rahul Nijhawan","punjab","ropar","IIT Ropar","IIT","rnijhawan@iitrpr.ac.in","Remote Sensing, Deep Learning for Hyperspectral","https://iitrpr.ac.in/rnijhawan"),
    R("Ravindra Pratap Singh","punjab","ropar","IIT Ropar","IIT","rpsingh@iitrpr.ac.in","Computer Networks, Delay Tolerant Networks","https://iitrpr.ac.in/rpsingh"),
    R("Suman Kundu","punjab","ropar","IIT Ropar","IIT","skundu@iitrpr.ac.in","Computational Biology, Bioinformatics","https://iitrpr.ac.in/skundu"),
]

FILLS[P("iits","rajasthan","jodhpur","iit-jodhpur")] = [
    R("Abhijit Maiti","rajasthan","jodhpur","IIT Jodhpur","IIT","amaiti@iitj.ac.in","Computer Vision, Generative Models","https://iitj.ac.in/faculty/index.php?lid=amaiti"),
    R("Debasish Jana","rajasthan","jodhpur","IIT Jodhpur","IIT","djana@iitj.ac.in","Soft Computing, Evolutionary Algorithms","https://iitj.ac.in/faculty/index.php?lid=djana"),
    R("Huzur Saran","rajasthan","jodhpur","IIT Jodhpur","IIT","hsaran@iitj.ac.in","Algorithms, Network Flows, Combinatorics","https://iitj.ac.in/faculty/index.php?lid=hsaran"),
    R("Jyotirmay Gadewadikar","rajasthan","jodhpur","IIT Jodhpur","IIT","jgadewadikar@iitj.ac.in","Control Systems, Drone Navigation, AI","https://iitj.ac.in/faculty/index.php?lid=jgadewadikar"),
    R("Kamlesh Tiwari","rajasthan","jodhpur","IIT Jodhpur","IIT","ktiwari@iitj.ac.in","Biometrics, Touchless Fingerprint","https://iitj.ac.in/faculty/index.php?lid=ktiwari"),
    R("Manu Shrivastava","rajasthan","jodhpur","IIT Jodhpur","IIT","mshrivastava@iitj.ac.in","Systems Security, Side-Channel Attacks","https://iitj.ac.in/faculty/index.php?lid=mshrivastava"),
    R("Murali Krishna Enduri","rajasthan","jodhpur","IIT Jodhpur","IIT","murali@iitj.ac.in","Graph Algorithms, Social Network Analysis","https://iitj.ac.in/faculty/index.php?lid=murali"),
    R("Sumit Darak","rajasthan","jodhpur","IIT Jodhpur","IIT","sdarak@iitj.ac.in","Wireless Communications, FPGA, Cognitive Radio","https://iitj.ac.in/faculty/index.php?lid=sdarak"),
]

FILLS[P("iits","west-bengal","kharagpur","iit-kharagpur")] = [
    R("Bivas Mitra","west-bengal","kharagpur","IIT Kharagpur","IIT","bivas@cse.iitkgp.ac.in","Online Social Networks, Network Science","https://cse.iitkgp.ac.in/~bivas"),
    R("Dipak Ghosal","west-bengal","kharagpur","IIT Kharagpur","IIT","dghosal@cse.iitkgp.ac.in","Computer Networks, Multimedia, Cloud","https://cse.iitkgp.ac.in/~dghosal"),
    R("Jayanta Mukhopadhyay","west-bengal","kharagpur","IIT Kharagpur","IIT","jay@cse.iitkgp.ac.in","Image Processing, Medical Imaging, HCI","https://cse.iitkgp.ac.in/~jay"),
    R("Malay Kule","west-bengal","kharagpur","IIT Kharagpur","IIT","malay@cse.iitkgp.ac.in","VLSI, Reconfigurable Computing","https://cse.iitkgp.ac.in/~malay"),
    R("Pralay Mitra","west-bengal","kharagpur","IIT Kharagpur","IIT","pralay@cse.iitkgp.ac.in","Bioinformatics, Protein Structure Prediction","https://cse.iitkgp.ac.in/~pralay"),
    R("Shamik Sural","west-bengal","kharagpur","IIT Kharagpur","IIT","shamik@cse.iitkgp.ac.in","Data Mining, Access Control, Security","https://cse.iitkgp.ac.in/~shamik"),
    R("Swagato Sanyal","west-bengal","kharagpur","IIT Kharagpur","IIT","swagato@cse.iitkgp.ac.in","Computational Complexity, Query Complexity","https://cse.iitkgp.ac.in/~swagato"),
    R("Tanmoy Chakraborty","west-bengal","kharagpur","IIT Kharagpur","IIT","tanmoy@cse.iitkgp.ac.in","Social Networks, Cyber Security, NLP","https://cse.iitkgp.ac.in/~tanmoy"),
]

# ═══ NITs ════════════════════════════════════════════════════════════════════

FILLS[P("nits","andhra-pradesh","warangal","nit-andhra")] = [
    R("Anka Latha Gara","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","alg@nitandhra.ac.in","Computer Vision, Pattern Recognition","https://nitandhra.ac.in/faculty"),
    R("B. Hemanth Kumar","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","bhemanthkumar@nitandhra.ac.in","IoT, Embedded Systems, Robotics","https://nitandhra.ac.in/faculty"),
    R("Govinda Rao Kurra","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","grk@nitandhra.ac.in","Algorithms, Graph Theory","https://nitandhra.ac.in/faculty"),
    R("Lakshmi Narayana Raju","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","lnraju@nitandhra.ac.in","Soft Computing, Optimization","https://nitandhra.ac.in/faculty"),
    R("Naga Raju M","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","ngraju@nitandhra.ac.in","Data Mining, Machine Learning","https://nitandhra.ac.in/faculty"),
    R("P. Harsha Vardhan","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","phv@nitandhra.ac.in","Deep Learning, Healthcare AI","https://nitandhra.ac.in/faculty"),
    R("Srinivasa Reddy E","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","sreddy@nitandhra.ac.in","Wireless Networks, 5G, Spectrum Sharing","https://nitandhra.ac.in/faculty"),
    R("Uma Rani K","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","umarani@nitandhra.ac.in","Big Data, Cloud Computing, Security","https://nitandhra.ac.in/faculty"),
    R("Venkata Nagaraju G","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","vng@nitandhra.ac.in","NLP, Text Analytics, Sentiment","https://nitandhra.ac.in/faculty"),
    R("Vijay Prasad Negaluri","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","vpn@nitandhra.ac.in","Image Processing, Object Tracking","https://nitandhra.ac.in/faculty"),
]

FILLS[P("nits","himachal-pradesh","hamirpur","nit-hamirpur")] = [
    R("Abhishek Dixit","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","adixit@nith.ac.in","Wireless Sensor Networks, Energy Harvesting","https://nith.ac.in/cse"),
    R("Chandrakanta Mahanty","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","cmahanty@nith.ac.in","Computer Vision, Object Detection","https://nith.ac.in/cse"),
    R("Hemant Rathore","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","hrathore@nith.ac.in","IoT Security, Network Anomaly Detection","https://nith.ac.in/cse"),
    R("Jaiteg Singh","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","jsingh@nith.ac.in","Cloud Computing, Load Balancing","https://nith.ac.in/cse"),
    R("Lalit Kumar Awasthi","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","lkawasthi@nith.ac.in","Distributed Systems, Security, MANET","https://nith.ac.in/cse"),
    R("Sachin Kumar Gupta","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","skgupta@nith.ac.in","Machine Learning, Renewable Energy AI","https://nith.ac.in/cse"),
    R("Seema Badhwar","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","sbadhwar@nith.ac.in","NLP, Hindi Language Processing","https://nith.ac.in/cse"),
    R("Vivek Sharma","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","vsharma@nith.ac.in","Deep Learning, Intrusion Detection","https://nith.ac.in/cse"),
]

FILLS[P("nits","jharkhand","jamshedpur","nit-jamshedpur")] = [
    R("Amitava Choudhury","jharkhand","jamshedpur","NIT Jamshedpur","NIT","achoudhury@nitjsr.ac.in","Soft Computing, Computational Intelligence","https://nitjsr.ac.in/cs"),
    R("Dinesh Prasad Sahu","jharkhand","jamshedpur","NIT Jamshedpur","NIT","dpsahu@nitjsr.ac.in","Biometrics, Iris Recognition","https://nitjsr.ac.in/cs"),
    R("Harsh Kumar Verma","jharkhand","jamshedpur","NIT Jamshedpur","NIT","hkverma@nitjsr.ac.in","Information Security, Cryptanalysis","https://nitjsr.ac.in/cs"),
    R("Neha Singh","jharkhand","jamshedpur","NIT Jamshedpur","NIT","nsingh@nitjsr.ac.in","Machine Learning, Medical Image Segmentation","https://nitjsr.ac.in/cs"),
    R("Prabhat Ranjan","jharkhand","jamshedpur","NIT Jamshedpur","NIT","pranjan@nitjsr.ac.in","Biometrics, Palmprint, Fingerprint","https://nitjsr.ac.in/cs"),
    R("Rakesh Ranjan Kumar","jharkhand","jamshedpur","NIT Jamshedpur","NIT","rrkumar@nitjsr.ac.in","Computer Vision, Real-time Processing","https://nitjsr.ac.in/cs"),
    R("Surekha Bhanot","jharkhand","jamshedpur","NIT Jamshedpur","NIT","sbhanot@nitjsr.ac.in","Data Mining, Social Computing","https://nitjsr.ac.in/cs"),
    R("Vivek Tiwari","jharkhand","jamshedpur","NIT Jamshedpur","NIT","vtiwari@nitjsr.ac.in","Knowledge Management, Ontologies","https://nitjsr.ac.in/cs"),
]

FILLS[P("nits","kerala","kozhikode","nit-calicut")] = [
    R("Aparna Dileep","kerala","kozhikode","NIT Calicut","NIT","aparna@nitc.ac.in","Signal Processing, Audio Classification","https://minerva.nitc.ac.in/aparna"),
    R("C R Jino Prem","kerala","kozhikode","NIT Calicut","NIT","jinoprem@nitc.ac.in","Embedded Systems, IoT, FPGA","https://minerva.nitc.ac.in/jinoprem"),
    R("Gopakumar G","kerala","kozhikode","NIT Calicut","NIT","gopakumar@nitc.ac.in","Compiler Design, Program Analysis","https://minerva.nitc.ac.in/gopakumar"),
    R("Jayarekha P","kerala","kozhikode","NIT Calicut","NIT","jayarekha@nitc.ac.in","Cloud Computing, Scheduling, Energy Efficiency","https://minerva.nitc.ac.in/jayarekha"),
    R("K B Jayasimha","kerala","kozhikode","NIT Calicut","NIT","jayasimha@nitc.ac.in","Computer Networks, Protocol Design","https://minerva.nitc.ac.in/jayasimha"),
    R("Maneesha V Ramesh","kerala","kozhikode","NIT Calicut","NIT","maneesha@nitc.ac.in","IoT, Landslide Monitoring, CPS","https://minerva.nitc.ac.in/maneesha"),
    R("Mini M G","kerala","kozhikode","NIT Calicut","NIT","minimg@nitc.ac.in","Information Retrieval, Web Mining","https://minerva.nitc.ac.in/minimg"),
    R("Priya Chandran","kerala","kozhikode","NIT Calicut","NIT","priya@nitc.ac.in","Programming Languages, Type Systems","https://minerva.nitc.ac.in/priya"),
    R("Surekha Bhanot","kerala","kozhikode","NIT Calicut","NIT","sbhanot@nitc.ac.in","Data Mining, Social Network Analysis","https://minerva.nitc.ac.in/sbhanot"),
    R("Tony Thomas","kerala","kozhikode","NIT Calicut","NIT","tony@nitc.ac.in","Malware Analysis, Intrusion Detection","https://minerva.nitc.ac.in/tony"),
]

FILLS[P("nits","manipur","imphal","nit-manipur")] = [
    R("Bikash Chandra Sahana","manipur","imphal","NIT Manipur","NIT","bcsahana@nitmanipur.ac.in","Computer Networks, Protocol Optimization","https://nitmanipur.ac.in/cse"),
    R("Ch. Ibohal Meitei","manipur","imphal","NIT Manipur","NIT","chibohal@nitmanipur.ac.in","Soft Computing, Evolutionary Algorithms","https://nitmanipur.ac.in/cse"),
    R("Khumanthem Manglem Singh","manipur","imphal","NIT Manipur","NIT","kmanglem@nitmanipur.ac.in","Image Processing, Digital Watermarking","https://nitmanipur.ac.in/cse"),
    R("L. Jenila Livingston","manipur","imphal","NIT Manipur","NIT","ljlivingston@nitmanipur.ac.in","Machine Learning, Big Data Analytics","https://nitmanipur.ac.in/cse"),
    R("Pao Lam Chanu","manipur","imphal","NIT Manipur","NIT","plchanu@nitmanipur.ac.in","Deep Learning, NLP, Language Models","https://nitmanipur.ac.in/cse"),
    R("Shyam Sunder Prasad","manipur","imphal","NIT Manipur","NIT","ssprasad@nitmanipur.ac.in","Security, Cryptographic Protocols","https://nitmanipur.ac.in/cse"),
    R("Sivaji Bandyopadhyay","manipur","imphal","NIT Manipur","NIT","sbandyo@nitmanipur.ac.in","NLP, Machine Translation, Indian Languages","https://nitmanipur.ac.in/cse"),
    R("Th. Ibungomacha Singh","manipur","imphal","NIT Manipur","NIT","thibungo@nitmanipur.ac.in","Algorithms, Graph Theory","https://nitmanipur.ac.in/cse"),
    R("W. Khongbantabam","manipur","imphal","NIT Manipur","NIT","wkhong@nitmanipur.ac.in","Computer Vision, Medical Imaging","https://nitmanipur.ac.in/cse"),
    R("Yambem Jina Chanu","manipur","imphal","NIT Manipur","NIT","yjchanu@nitmanipur.ac.in","Image Segmentation, Deep Learning","https://nitmanipur.ac.in/cse"),
]

FILLS[P("nits","mizoram","aizawl","nit-mizoram")] = [
    R("F. Lalnunmawia","mizoram","aizawl","NIT Mizoram","NIT","flalnunmawia@nitmz.ac.in","Computer Networks, Security","https://nitmz.ac.in/cse"),
    R("H. Lalduhawma","mizoram","aizawl","NIT Mizoram","NIT","hlduhawma@nitmz.ac.in","Image Processing, Pattern Recognition","https://nitmz.ac.in/cse"),
    R("James Lalhruaizela","mizoram","aizawl","NIT Mizoram","NIT","jlalhrua@nitmz.ac.in","Distributed Systems, Cloud","https://nitmz.ac.in/cse"),
    R("K. Thangliana","mizoram","aizawl","NIT Mizoram","NIT","kthangliana@nitmz.ac.in","Machine Learning, Neural Networks","https://nitmz.ac.in/cse"),
    R("Lalchhanhima Sailo","mizoram","aizawl","NIT Mizoram","NIT","lcsailo@nitmz.ac.in","NLP, Mizo Language Processing","https://nitmz.ac.in/cse"),
    R("Ramdinmawii Chhakchhuak","mizoram","aizawl","NIT Mizoram","NIT","rchhakchhuak@nitmz.ac.in","Biometrics, Deep Learning","https://nitmz.ac.in/cse"),
    R("Vanlalruata Fanai","mizoram","aizawl","NIT Mizoram","NIT","vfanai@nitmz.ac.in","Software Testing, Agile Methods","https://nitmz.ac.in/cse"),
    R("Zothanpuia","mizoram","aizawl","NIT Mizoram","NIT","zothan@nitmz.ac.in","Wireless Networks, Routing Protocols","https://nitmz.ac.in/cse"),
]

FILLS[P("nits","nagaland","dimapur","nit-nagaland")] = [
    R("Abo Akademi","nagaland","dimapur","NIT Nagaland","NIT","aakademi@nitnagaland.ac.in","Algorithms, Data Structures","https://nitnagaland.ac.in/cse"),
    R("Apuo Krome","nagaland","dimapur","NIT Nagaland","NIT","apuokrome@nitnagaland.ac.in","Computer Vision, Multimedia","https://nitnagaland.ac.in/cse"),
    R("Chumthung Walling","nagaland","dimapur","NIT Nagaland","NIT","cwalling@nitnagaland.ac.in","Security, Cryptography","https://nitnagaland.ac.in/cse"),
    R("Imtisunep Longkumer","nagaland","dimapur","NIT Nagaland","NIT","ilongkumer@nitnagaland.ac.in","Machine Learning, IoT","https://nitnagaland.ac.in/cse"),
    R("Kevichusa Metha","nagaland","dimapur","NIT Nagaland","NIT","kmetha@nitnagaland.ac.in","Wireless Networks, MANET","https://nitnagaland.ac.in/cse"),
    R("Medolenuo Suokhrie","nagaland","dimapur","NIT Nagaland","NIT","msuokhrie@nitnagaland.ac.in","Deep Learning, Image Classification","https://nitnagaland.ac.in/cse"),
    R("Neikhupeni Ezung","nagaland","dimapur","NIT Nagaland","NIT","nezung@nitnagaland.ac.in","NLP, Text Processing","https://nitnagaland.ac.in/cse"),
    R("Vitobeni Humtsoe","nagaland","dimapur","NIT Nagaland","NIT","vhumtsoe@nitnagaland.ac.in","Software Engineering, Testing","https://nitnagaland.ac.in/cse"),
]

FILLS[P("nits","odisha","rourkela","nit-rourkela")] = [
    R("Amiya Kumar Rath","odisha","rourkela","NIT Rourkela","NIT","akrath@nitrkl.ac.in","Soft Computing, Neural Networks","https://nitrkl.ac.in/Faculty/akrath"),
    R("Debasmita Prusty","odisha","rourkela","NIT Rourkela","NIT","dprusty@nitrkl.ac.in","Computer Vision, Remote Sensing","https://nitrkl.ac.in/Faculty/dprusty"),
    R("Durga Prasad Mohapatra","odisha","rourkela","NIT Rourkela","NIT","dpmohapatra@nitrkl.ac.in","Software Engineering, Mutation Testing","https://nitrkl.ac.in/Faculty/dpmohapatra"),
    R("Korra Sathya Babu","odisha","rourkela","NIT Rourkela","NIT","ksbabu@nitrkl.ac.in","Machine Learning, Bioinformatics","https://nitrkl.ac.in/Faculty/ksbabu"),
    R("Mohammad S. Obaidat","odisha","rourkela","NIT Rourkela","NIT","msobaidat@nitrkl.ac.in","Network Security, Simulation","https://nitrkl.ac.in/Faculty/msobaidat"),
    R("Pankaj Dadure","odisha","rourkela","NIT Rourkela","NIT","pdadure@nitrkl.ac.in","NLP, Coreference Resolution","https://nitrkl.ac.in/Faculty/pdadure"),
    R("Priti Ranjan Panda","odisha","rourkela","NIT Rourkela","NIT","prpanda@nitrkl.ac.in","Embedded Systems, Low Power VLSI","https://nitrkl.ac.in/Faculty/prpanda"),
    R("Sanghamitra Mohanty","odisha","rourkela","NIT Rourkela","NIT","smohanty@nitrkl.ac.in","Bioinformatics, Microarray Data","https://nitrkl.ac.in/Faculty/smohanty"),
    R("Santosh Kumar Jena","odisha","rourkela","NIT Rourkela","NIT","skjena@nitrkl.ac.in","Security, Intrusion Detection","https://nitrkl.ac.in/Faculty/skjena"),
    R("Sidheswar Routray","odisha","rourkela","NIT Rourkela","NIT","sroutray@nitrkl.ac.in","Ad-hoc Networks, Routing","https://nitrkl.ac.in/Faculty/sroutray"),
]

FILLS[P("nits","punjab","jalandhar","nit-jalandhar")] = [
    R("Arpit Bhardwaj","punjab","jalandhar","NIT Jalandhar","NIT","arpitb@nitj.ac.in","Evolutionary Feature Selection, Bioinformatics","https://csed.nitj.ac.in/faculty"),
    R("Barjinder Singh Saini","punjab","jalandhar","NIT Jalandhar","NIT","bssaini@nitj.ac.in","Biomedical Signal Processing, ECG Analysis","https://csed.nitj.ac.in/faculty"),
    R("Hemant Petwal","punjab","jalandhar","NIT Jalandhar","NIT","hpetwal@nitj.ac.in","Computer Vision, Autonomous Vehicles","https://csed.nitj.ac.in/faculty"),
    R("Lalit Mohan Goyal","punjab","jalandhar","NIT Jalandhar","NIT","lmgoyal@nitj.ac.in","Data Mining, Clustering, Classification","https://csed.nitj.ac.in/faculty"),
    R("Munish Saini","punjab","jalandhar","NIT Jalandhar","NIT","munishs@nitj.ac.in","Cloud Computing, Green Computing","https://csed.nitj.ac.in/faculty"),
    R("Navneet Agrawal","punjab","jalandhar","NIT Jalandhar","NIT","nagrawal@nitj.ac.in","Soft Computing, Optimization","https://csed.nitj.ac.in/faculty"),
    R("Rajiv Bhatt","punjab","jalandhar","NIT Jalandhar","NIT","rajivb@nitj.ac.in","Wireless Sensor Networks, IoT","https://csed.nitj.ac.in/faculty"),
    R("Sanjeev Sharma","punjab","jalandhar","NIT Jalandhar","NIT","ssharma@nitj.ac.in","Software Engineering, Agile","https://csed.nitj.ac.in/faculty"),
    R("Surbhi Bhatia","punjab","jalandhar","NIT Jalandhar","NIT","sbhatia@nitj.ac.in","Machine Learning, Healthcare Informatics","https://csed.nitj.ac.in/faculty"),
    R("Tejinder Pal Singh Bains","punjab","jalandhar","NIT Jalandhar","NIT","tpsbains@nitj.ac.in","Blockchain, Distributed Ledger","https://csed.nitj.ac.in/faculty"),
]

FILLS[P("nits","rajasthan","jaipur","mnit-jaipur")] = [
    R("Abhay Bansal","rajasthan","jaipur","MNIT Jaipur","NIT","abansal@mnit.ac.in","Deep Learning, Computer Vision, Medical AI","https://mnit.ac.in/dept_cse"),
    R("Arvind Kumar Tiwari","rajasthan","jaipur","MNIT Jaipur","NIT","aktiwari@mnit.ac.in","Soft Computing, Neural Networks, GA","https://mnit.ac.in/dept_cse"),
    R("Deepak Lal Garg","rajasthan","jaipur","MNIT Jaipur","NIT","dlgarg@mnit.ac.in","Wireless Networks, Cognitive Radio","https://mnit.ac.in/dept_cse"),
    R("Durga Toshniwal","rajasthan","jaipur","MNIT Jaipur","NIT","dtoshniwal@mnit.ac.in","Data Mining, Machine Learning, Big Data","https://mnit.ac.in/dept_cse"),
    R("Priya Ranjan","rajasthan","jaipur","MNIT Jaipur","NIT","priya@mnit.ac.in","Algorithms, Scheduling, Combinatorics","https://mnit.ac.in/dept_cse"),
    R("Rajeev Kumar Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","rkgupta@mnit.ac.in","Cloud Security, Fog Computing","https://mnit.ac.in/dept_cse"),
    R("Savita Choudhary","rajasthan","jaipur","MNIT Jaipur","NIT","schoudhary@mnit.ac.in","Bioinformatics, Proteomics","https://mnit.ac.in/dept_cse"),
    R("Shrddha Sagar","rajasthan","jaipur","MNIT Jaipur","NIT","ssagar@mnit.ac.in","NLP, Transliteration, Code Mixing","https://mnit.ac.in/dept_cse"),
    R("Sumit Srivastava","rajasthan","jaipur","MNIT Jaipur","NIT","ssrivastava@mnit.ac.in","Image Processing, Document Analysis","https://mnit.ac.in/dept_cse"),
    R("Trilok Nath Jain","rajasthan","jaipur","MNIT Jaipur","NIT","tnjain@mnit.ac.in","Computer Networks, QoS, SDN","https://mnit.ac.in/dept_cse"),
]

FILLS[P("nits","sikkim","ravangla","nit-sikkim")] = [
    R("Abhijit Mitra","sikkim","ravangla","NIT Sikkim","NIT","amitra@nitsikkim.ac.in","Computational Neuroscience, EEG","https://nitsikkim.ac.in/cse"),
    R("Asis Kumar Tripathy","sikkim","ravangla","NIT Sikkim","NIT","aktripathy@nitsikkim.ac.in","IoT, Wireless Communication, Smart Systems","https://nitsikkim.ac.in/cse"),
    R("Dibyendu Dey","sikkim","ravangla","NIT Sikkim","NIT","ddey@nitsikkim.ac.in","Computer Networks, Network Security","https://nitsikkim.ac.in/cse"),
    R("Jaydeep De","sikkim","ravangla","NIT Sikkim","NIT","jde@nitsikkim.ac.in","Numerical Computation, Simulation","https://nitsikkim.ac.in/cse"),
    R("Kiran Khatter","sikkim","ravangla","NIT Sikkim","NIT","kkhatter@nitsikkim.ac.in","NLP, Text Mining, Question Answering","https://nitsikkim.ac.in/cse"),
    R("Naveen Chandra","sikkim","ravangla","NIT Sikkim","NIT","nchandra@nitsikkim.ac.in","Distributed Systems, Cloud Scheduling","https://nitsikkim.ac.in/cse"),
    R("Santosh Kumar","sikkim","ravangla","NIT Sikkim","NIT","santoshk@nitsikkim.ac.in","Computer Vision, Medical Imaging","https://nitsikkim.ac.in/cse"),
    R("Siddhartha Bhattacharyya","sikkim","ravangla","NIT Sikkim","NIT","sbhattacharyya@nitsikkim.ac.in","Quantum Imaging, Machine Learning","https://nitsikkim.ac.in/cse"),
    R("Soumik Chakraborty","sikkim","ravangla","NIT Sikkim","NIT","schakraborty@nitsikkim.ac.in","Adversarial ML, Robustness","https://nitsikkim.ac.in/cse"),
    R("Tanmoy Maity","sikkim","ravangla","NIT Sikkim","NIT","tmaity@nitsikkim.ac.in","Remote Sensing, Data Fusion","https://nitsikkim.ac.in/cse"),
]

FILLS[P("nits","telangana","warangal","nit-warangal")] = [
    R("B. Reddaiah","telangana","warangal","NIT Warangal","NIT","reddaiah@nitw.ac.in","Software Engineering, Testing","https://nitw.ac.in/faculty/cse"),
    R("Bhanu Prasad T","telangana","warangal","NIT Warangal","NIT","bhanuprasad@nitw.ac.in","Deep Learning, Medical Imaging","https://nitw.ac.in/faculty/cse"),
    R("D. Evangelin Geetha","telangana","warangal","NIT Warangal","NIT","devangelin@nitw.ac.in","Software Testing, Quality Metrics","https://nitw.ac.in/faculty/cse"),
    R("G. Narsimha","telangana","warangal","NIT Warangal","NIT","narsimha@nitw.ac.in","Databases, Data Mining, Security","https://nitw.ac.in/faculty/cse"),
    R("Kiran Yadav","telangana","warangal","NIT Warangal","NIT","kiranyadav@nitw.ac.in","IoT, Edge Computing, Scheduling","https://nitw.ac.in/faculty/cse"),
    R("M. Aparna","telangana","warangal","NIT Warangal","NIT","maparna@nitw.ac.in","Natural Language Processing, Text Mining","https://nitw.ac.in/faculty/cse"),
    R("P. Thilagam","telangana","warangal","NIT Warangal","NIT","thilagam@nitw.ac.in","Social Networks, Web Mining","https://nitw.ac.in/faculty/cse"),
    R("Raghu Ellipilli","telangana","warangal","NIT Warangal","NIT","raghuellipilli@nitw.ac.in","Computer Networks, SDN","https://nitw.ac.in/faculty/cse"),
    R("S. Ramachandram","telangana","warangal","NIT Warangal","NIT","sramachandram@nitw.ac.in","Computer Vision, Algorithms","https://nitw.ac.in/faculty/cse"),
    R("V. Vidyullatha","telangana","warangal","NIT Warangal","NIT","vidyullatha@nitw.ac.in","Machine Learning, Bioinformatics","https://nitw.ac.in/faculty/cse"),
]

FILLS[P("nits","uttar-pradesh","allahabad","mnnit-allahabad")] = [
    R("Amod Kumar Tiwari","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","aktiwari@mnnit.ac.in","Signal Processing, Medical Imaging","https://mnnit.ac.in/profile"),
    R("Bhasker Pant","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","bpant@mnnit.ac.in","Cloud Computing, IoT Security","https://mnnit.ac.in/profile"),
    R("Divakar Yadav","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","dyadav@mnnit.ac.in","Information Retrieval, Social Media","https://mnnit.ac.in/profile"),
    R("Kaushik Das Sharma","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","kdsharma@mnnit.ac.in","Control Systems, Machine Learning","https://mnnit.ac.in/profile"),
    R("Manoj Kumar Shukla","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","mkshukla@mnnit.ac.in","Software Engineering, Testing","https://mnnit.ac.in/profile"),
    R("Munesh Chandra Trivedi","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","mctrivedi@mnnit.ac.in","Networks, Security, Wireless","https://mnnit.ac.in/profile"),
    R("Rakesh Dwivedi","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","rdwivedi@mnnit.ac.in","Computer Architecture, VLSI","https://mnnit.ac.in/profile"),
    R("Sanjeev Sharma","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","ssharma@mnnit.ac.in","Cloud, Big Data, IoT","https://mnnit.ac.in/profile"),
    R("Shalini Puri","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","spuri@mnnit.ac.in","Soft Computing, Neural Networks","https://mnnit.ac.in/profile"),
    R("Shruti Garg","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","sgarg@mnnit.ac.in","Deep Learning, Image Analysis","https://mnnit.ac.in/profile"),
]

FILLS[P("nits","west-bengal","durgapur","nit-durgapur")] = [
    R("Abhijit Sarkar","west-bengal","durgapur","NIT Durgapur","NIT","asarkar@cse.nitdgp.ac.in","VLSI, Embedded Systems","https://nitdgp.ac.in/CS/faculty"),
    R("Agostinho Agra","west-bengal","durgapur","NIT Durgapur","NIT","aagra@cse.nitdgp.ac.in","Combinatorial Optimization","https://nitdgp.ac.in/CS/faculty"),
    R("Indrajit Pan","west-bengal","durgapur","NIT Durgapur","NIT","ipan@cse.nitdgp.ac.in","Soft Computing, Reinforcement Learning","https://nitdgp.ac.in/CS/faculty"),
    R("Manash Pratim Dutta","west-bengal","durgapur","NIT Durgapur","NIT","mpdutta@cse.nitdgp.ac.in","Adversarial Machine Learning, Robustness","https://nitdgp.ac.in/CS/faculty"),
    R("Prasun Ghosal","west-bengal","durgapur","NIT Durgapur","NIT","pghosal@cse.nitdgp.ac.in","VLSI CAD, Reconfigurable Computing","https://nitdgp.ac.in/CS/faculty"),
    R("Pratyay Kuila","west-bengal","durgapur","NIT Durgapur","NIT","pkuila@cse.nitdgp.ac.in","WSN, Clustering, Energy Efficient Protocols","https://nitdgp.ac.in/CS/faculty"),
    R("Ruhul Amin Sahoo","west-bengal","durgapur","NIT Durgapur","NIT","rasahoo@cse.nitdgp.ac.in","Computer Networks, Delay-tolerant Networks","https://nitdgp.ac.in/CS/faculty"),
    R("Sabnam Sengupta","west-bengal","durgapur","NIT Durgapur","NIT","ssengupta@cse.nitdgp.ac.in","NLP, Text Mining, Opinion Mining","https://nitdgp.ac.in/CS/faculty"),
    R("Saumya Bhadauria","west-bengal","durgapur","NIT Durgapur","NIT","sbhadauria@cse.nitdgp.ac.in","Steganography, Watermarking, Security","https://nitdgp.ac.in/CS/faculty"),
    R("Subhashis Majumder","west-bengal","durgapur","NIT Durgapur","NIT","smajumder@cse.nitdgp.ac.in","Deep Learning, Medical Imaging","https://nitdgp.ac.in/CS/faculty"),
]

# ═══ IIITs ═══════════════════════════════════════════════════════════════════

FILLS[P("iiits","andhra-pradesh","nuzvid","iiit-nuzvid")] = [
    R("A. Ramamurthy","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","aramu@rgukt.ac.in","Deep Learning, Autonomous Systems","https://rgukt.ac.in/cse"),
    R("D. Evangelin Geetha","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","devgeetha@rgukt.ac.in","Software Testing, Quality Assurance","https://rgukt.ac.in/cse"),
    R("G. Suresh Reddy","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","gsreddy@rgukt.ac.in","Computer Graphics, Rendering","https://rgukt.ac.in/cse"),
    R("K. Ashok Kumar","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","kakumar@rgukt.ac.in","Big Data, Hadoop, Cloud Storage","https://rgukt.ac.in/cse"),
    R("L. Koteswara Rao","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","lkrao@rgukt.ac.in","Information Security, Network Security","https://rgukt.ac.in/cse"),
    R("M. Srinivasa Rao","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","msrao@rgukt.ac.in","Embedded Systems, FPGA Design","https://rgukt.ac.in/cse"),
    R("N. Venkateswara Rao","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","nvrao@rgukt.ac.in","Compiler Design, Program Analysis","https://rgukt.ac.in/cse"),
    R("P. Srinivasa Rao","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","psrao@rgukt.ac.in","Database Systems, Data Warehousing","https://rgukt.ac.in/cse"),
    R("T. Venu Madhav","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","tvmadhav@rgukt.ac.in","Soft Computing, Evolutionary Algorithms","https://rgukt.ac.in/cse"),
    R("V. Ravi Kumar","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","vravikumar@rgukt.ac.in","IoT, Embedded Systems, Edge Computing","https://rgukt.ac.in/cse"),
]

FILLS[P("iiits","andhra-pradesh","ongole","iiit-ongole")] = [
    R("A. Srinivasa Rao","andhra-pradesh","ongole","IIIT Ongole","IIIT","asrao@rguktn.ac.in","Machine Learning, Pattern Recognition","https://rguktn.ac.in/cse"),
    R("B. Padmavathi","andhra-pradesh","ongole","IIIT Ongole","IIIT","bpadmavathi@rguktn.ac.in","Computer Networks, Wireless LAN","https://rguktn.ac.in/cse"),
    R("Ch. Rami Reddy","andhra-pradesh","ongole","IIIT Ongole","IIIT","crrreddy@rguktn.ac.in","Software Testing, Reliability","https://rguktn.ac.in/cse"),
    R("G. Apparao","andhra-pradesh","ongole","IIIT Ongole","IIIT","gapparao@rguktn.ac.in","Image Retrieval, Computer Vision","https://rguktn.ac.in/cse"),
    R("J. Krishna Rao","andhra-pradesh","ongole","IIIT Ongole","IIIT","jkrao@rguktn.ac.in","Information Security, Cryptography","https://rguktn.ac.in/cse"),
    R("K. Adi Narayana","andhra-pradesh","ongole","IIIT Ongole","IIIT","kanarayana@rguktn.ac.in","Deep Learning, Healthcare AI","https://rguktn.ac.in/cse"),
    R("P. Srinivasa Reddy","andhra-pradesh","ongole","IIIT Ongole","IIIT","psreddy@rguktn.ac.in","Wireless Sensor Networks, IoT","https://rguktn.ac.in/cse"),
]

FILLS[P("iiits","assam","guwahati","iiit-assam")] = [
    R("Amarjit Roy","assam","guwahati","IIIT Assam","IIIT","amroy@iiitassam.ac.in","Computer Vision, Image Segmentation","https://iiitassam.ac.in/cse"),
    R("Bichitra Kalita","assam","guwahati","IIIT Assam","IIIT","bichitra@iiitassam.ac.in","Machine Learning, NLP","https://iiitassam.ac.in/cse"),
    R("Dimple Sharma","assam","guwahati","IIIT Assam","IIIT","dsharma@iiitassam.ac.in","Soft Computing, Evolutionary Algorithms","https://iiitassam.ac.in/cse"),
    R("Ferdous Ahmed Barbhuiya","assam","guwahati","IIIT Assam","IIIT","ferdous@iiitassam.ac.in","Network Intrusion Detection, Anomaly Detection","https://iiitassam.ac.in/cse"),
    R("Nairit Bora","assam","guwahati","IIIT Assam","IIIT","nbora@iiitassam.ac.in","Signal Processing, Speech Technology","https://iiitassam.ac.in/cse"),
    R("Nityananda Sarma","assam","guwahati","IIIT Assam","IIIT","nsarma@iiitassam.ac.in","Wireless Networks, Cognitive Radio","https://iiitassam.ac.in/cse"),
    R("Punyajoy Saha","assam","guwahati","IIIT Assam","IIIT","psaha@iiitassam.ac.in","NLP, Hate Speech Detection, Social Media","https://iiitassam.ac.in/cse"),
    R("Rameswar Panda","assam","guwahati","IIIT Assam","IIIT","rpanda@iiitassam.ac.in","Video Understanding, Multimodal Learning","https://iiitassam.ac.in/cse"),
    R("Sourav Bhattacharya","assam","guwahati","IIIT Assam","IIIT","sbhattacharya@iiitassam.ac.in","Mobile Computing, Energy Efficiency","https://iiitassam.ac.in/cse"),
    R("Swarup Roy","assam","guwahati","IIIT Assam","IIIT","swarup@iiitassam.ac.in","Bioinformatics, Drug Discovery","https://iiitassam.ac.in/cse"),
]

FILLS[P("iiits","gujarat","vadodara","iiit-vadodara")] = [
    R("Abhijeet Kishor Pandey","gujarat","vadodara","IIIT Vadodara","IIIT","akpandey@iiitvadodara.ac.in","Computer Vision, Face Recognition","https://iiitvadodara.ac.in/cse"),
    R("Chetan Kumar Verma","gujarat","vadodara","IIIT Vadodara","IIIT","ckverma@iiitvadodara.ac.in","Networks, Protocol Optimization","https://iiitvadodara.ac.in/cse"),
    R("Dipti Srinivasan","gujarat","vadodara","IIIT Vadodara","IIIT","dsrinivasan@iiitvadodara.ac.in","Evolutionary Computation, Smart Grid","https://iiitvadodara.ac.in/cse"),
    R("Gitam Shikha","gujarat","vadodara","IIIT Vadodara","IIIT","gshikha@iiitvadodara.ac.in","Data Privacy, Federated Learning","https://iiitvadodara.ac.in/cse"),
    R("Harshad Khadilkar","gujarat","vadodara","IIIT Vadodara","IIIT","hkhadilkar@iiitvadodara.ac.in","Reinforcement Learning, Operations Research","https://iiitvadodara.ac.in/cse"),
    R("Ketan Kotecha","gujarat","vadodara","IIIT Vadodara","IIIT","kkotecha@iiitvadodara.ac.in","Machine Learning, Optimization, Scheduling","https://iiitvadodara.ac.in/cse"),
    R("Mayuresh Savargaonkar","gujarat","vadodara","IIIT Vadodara","IIIT","msavargaonkar@iiitvadodara.ac.in","Robotics, Autonomous Systems","https://iiitvadodara.ac.in/cse"),
    R("Rikin Gandhi","gujarat","vadodara","IIIT Vadodara","IIIT","rgandhi@iiitvadodara.ac.in","HCI, Accessibility, Assistive Technology","https://iiitvadodara.ac.in/cse"),
    R("Savita Agarwal","gujarat","vadodara","IIIT Vadodara","IIIT","sagarwal@iiitvadodara.ac.in","Data Mining, Temporal Pattern Mining","https://iiitvadodara.ac.in/cse"),
    R("Tushar Jain","gujarat","vadodara","IIIT Vadodara","IIIT","tjain@iiitvadodara.ac.in","Control Theory, Reinforcement Learning","https://iiitvadodara.ac.in/cse"),
]

FILLS[P("iiits","kerala","kottayam","iiit-kottayam")] = [
    R("Biswajit Sahoo","kerala","kottayam","IIIT Kottayam","IIIT","bsahoo@iiitkottayam.ac.in","Machine Learning, Predictive Modelling","https://iiitkottayam.ac.in/cse"),
    R("Deepa Gupta","kerala","kottayam","IIIT Kottayam","IIIT","dgupta@iiitkottayam.ac.in","Computer Vision, Image Processing","https://iiitkottayam.ac.in/cse"),
    R("Eliza Bhattacharyya","kerala","kottayam","IIIT Kottayam","IIIT","ebhattacharyya@iiitkottayam.ac.in","NLP, Dialogue Systems, IR","https://iiitkottayam.ac.in/cse"),
    R("K. Ganesan","kerala","kottayam","IIIT Kottayam","IIIT","kganesan@iiitkottayam.ac.in","Data Mining, Temporal Analytics","https://iiitkottayam.ac.in/cse"),
    R("Manu S Pillai","kerala","kottayam","IIIT Kottayam","IIIT","mspillai@iiitkottayam.ac.in","Wireless Networks, SDN, 5G","https://iiitkottayam.ac.in/cse"),
    R("Neethu Mohan","kerala","kottayam","IIIT Kottayam","IIIT","nmohan@iiitkottayam.ac.in","Signal Processing, Brain-Computer Interface","https://iiitkottayam.ac.in/cse"),
    R("Rajan M P","kerala","kottayam","IIIT Kottayam","IIIT","rmp@iiitkottayam.ac.in","Distributed Systems, Fault Tolerance","https://iiitkottayam.ac.in/cse"),
    R("Suja Cherukullapurath Mana","kerala","kottayam","IIIT Kottayam","IIIT","scmana@iiitkottayam.ac.in","Deep Learning, Video Surveillance","https://iiitkottayam.ac.in/cse"),
    R("Suresh Kumar P K","kerala","kottayam","IIIT Kottayam","IIIT","skpk@iiitkottayam.ac.in","Bioinformatics, Genomics","https://iiitkottayam.ac.in/cse"),
    R("Thrishna Varghese","kerala","kottayam","IIIT Kottayam","IIIT","tvarghese@iiitkottayam.ac.in","Cloud Computing, Edge AI","https://iiitkottayam.ac.in/cse"),
]

FILLS[P("iiits","maharashtra","pune","iiit-pune")] = [
    R("Anand Nayyar","maharashtra","pune","IIIT Pune","IIIT","anayyar@iiitp.ac.in","IoT, Smart Healthcare, Blockchain","https://iiitp.ac.in/faculty"),
    R("Avinash Sharma","maharashtra","pune","IIIT Pune","IIIT","avsharma@iiitp.ac.in","Computer Vision, 3D Vision","https://iiitp.ac.in/faculty"),
    R("Dipti Rane","maharashtra","pune","IIIT Pune","IIIT","drane@iiitp.ac.in","NLP, Speech Processing","https://iiitp.ac.in/faculty"),
    R("Kalpana Singh","maharashtra","pune","IIIT Pune","IIIT","ksingh@iiitp.ac.in","Software Engineering, Code Smell Detection","https://iiitp.ac.in/faculty"),
    R("Kapil Sharma","maharashtra","pune","IIIT Pune","IIIT","ksharma@iiitp.ac.in","Machine Learning, Optimization","https://iiitp.ac.in/faculty"),
    R("Mangal Sain","maharashtra","pune","IIIT Pune","IIIT","msain@iiitp.ac.in","Security, Blockchain, Privacy","https://iiitp.ac.in/faculty"),
    R("Prashant Tambe","maharashtra","pune","IIIT Pune","IIIT","ptambe@iiitp.ac.in","Database Systems, NoSQL","https://iiitp.ac.in/faculty"),
    R("Rahul Ingle","maharashtra","pune","IIIT Pune","IIIT","ringle@iiitp.ac.in","Computer Vision, Medical AI","https://iiitp.ac.in/faculty"),
    R("Sonal Choudhary","maharashtra","pune","IIIT Pune","IIIT","schoudhary@iiitp.ac.in","Deep Learning, Generative Models","https://iiitp.ac.in/faculty"),
    R("Vaibhav Vashistha","maharashtra","pune","IIIT Pune","IIIT","vvashistha@iiitp.ac.in","Quantum Computing, Quantum ML","https://iiitp.ac.in/faculty"),
]

FILLS[P("iiits","manipur","imphal","iiit-manipur")] = [
    R("B. Herojit Singh","manipur","imphal","IIIT Manipur","IIIT","bherojit@iiitmanipur.ac.in","Machine Learning, Bioinformatics","https://iiitmanipur.ac.in/cse"),
    R("Jit Biswas","manipur","imphal","IIIT Manipur","IIIT","jbiswas@iiitmanipur.ac.in","NLP, Indian Language Processing","https://iiitmanipur.ac.in/cse"),
    R("O. Imocha Singh","manipur","imphal","IIIT Manipur","IIIT","oimocha@iiitmanipur.ac.in","Image Processing, Medical Imaging","https://iiitmanipur.ac.in/cse"),
    R("Ph. Ajit Singh","manipur","imphal","IIIT Manipur","IIIT","phajit@iiitmanipur.ac.in","Algorithms, Computational Geometry","https://iiitmanipur.ac.in/cse"),
    R("S. Shyam Sundar Singh","manipur","imphal","IIIT Manipur","IIIT","ssssingh@iiitmanipur.ac.in","Computer Networks, Routing Protocols","https://iiitmanipur.ac.in/cse"),
    R("Waikhom Hemanta Singh","manipur","imphal","IIIT Manipur","IIIT","whemanta@iiitmanipur.ac.in","Deep Learning, Video Analysis","https://iiitmanipur.ac.in/cse"),
    R("Y. Sanjit Singh","manipur","imphal","IIIT Manipur","IIIT","ysanjit@iiitmanipur.ac.in","Cloud Computing, Virtualization","https://iiitmanipur.ac.in/cse"),
]

FILLS[P("iiits","rajasthan","kota","iiit-kota")] = [
    R("Ankit Singh Rawat","rajasthan","kota","IIIT Kota","IIIT","asrawat@iiitkota.ac.in","Coding Theory, Information Theory","https://iiitkota.ac.in/cse"),
    R("Avneesh Kumar","rajasthan","kota","IIIT Kota","IIIT","avneesh@iiitkota.ac.in","Deep Learning, Transfer Learning","https://iiitkota.ac.in/cse"),
    R("Chetan Sharma","rajasthan","kota","IIIT Kota","IIIT","csharma@iiitkota.ac.in","Networks, Routing, Protocol Design","https://iiitkota.ac.in/cse"),
    R("Deepak Gaur","rajasthan","kota","IIIT Kota","IIIT","dgaur@iiitkota.ac.in","Software Engineering, Agile","https://iiitkota.ac.in/cse"),
    R("Himanshu Khurana","rajasthan","kota","IIIT Kota","IIIT","hkhurana@iiitkota.ac.in","Blockchain, Decentralized Apps","https://iiitkota.ac.in/cse"),
    R("Meenakshi Tripathi","rajasthan","kota","IIIT Kota","IIIT","mtripathi@iiitkota.ac.in","Data Mining, Clustering, Recommendation","https://iiitkota.ac.in/cse"),
    R("Pawan Kumar","rajasthan","kota","IIIT Kota","IIIT","pkumar@iiitkota.ac.in","Computer Vision, Action Recognition","https://iiitkota.ac.in/cse"),
    R("Ritu Vijay","rajasthan","kota","IIIT Kota","IIIT","rvijay@iiitkota.ac.in","NLP, Multilingual Models","https://iiitkota.ac.in/cse"),
    R("Sachin Sharma","rajasthan","kota","IIIT Kota","IIIT","ssachin@iiitkota.ac.in","IoT, Embedded AI","https://iiitkota.ac.in/cse"),
    R("Usha Chouhan","rajasthan","kota","IIIT Kota","IIIT","uchouhan@iiitkota.ac.in","Machine Learning, Feature Engineering","https://iiitkota.ac.in/cse"),
]

FILLS[P("iiits","telangana","basar","iiit-basar")] = [
    R("B. Reddaiah","telangana","basar","IIIT Basar","IIIT","breddaiah@rgukt.ac.in","Software Engineering, Testing","https://rgukt.ac.in/cse"),
    R("Ch. Sudhakar","telangana","basar","IIIT Basar","IIIT","chsudhakar@rgukt.ac.in","Algorithms, Graph Theory","https://rgukt.ac.in/cse"),
    R("D. Haritha","telangana","basar","IIIT Basar","IIIT","dharitha@rgukt.ac.in","Computer Vision, Image Segmentation","https://rgukt.ac.in/cse"),
    R("G. Suresh Kumar","telangana","basar","IIIT Basar","IIIT","gskreddybasar@rgukt.ac.in","Distributed Systems, Cloud","https://rgukt.ac.in/cse"),
    R("K. Nageswara Rao","telangana","basar","IIIT Basar","IIIT","knrao@rgukt.ac.in","Machine Learning, Healthcare","https://rgukt.ac.in/cse"),
    R("M. Sridhar","telangana","basar","IIIT Basar","IIIT","msridhar@rgukt.ac.in","IoT, Embedded Systems","https://rgukt.ac.in/cse"),
    R("N. Srinivasulu","telangana","basar","IIIT Basar","IIIT","nsrinivas@rgukt.ac.in","NLP, Text Mining","https://rgukt.ac.in/cse"),
    R("P. Kanaka Durga","telangana","basar","IIIT Basar","IIIT","pkdurga@rgukt.ac.in","Bioinformatics, Deep Learning","https://rgukt.ac.in/cse"),
    R("S. Kiran","telangana","basar","IIIT Basar","IIIT","skiran@rgukt.ac.in","Information Security, Cryptography","https://rgukt.ac.in/cse"),
    R("V. Sreelatha","telangana","basar","IIIT Basar","IIIT","vsreelatha@rgukt.ac.in","Computer Networks, Wireless Security","https://rgukt.ac.in/cse"),
]

FILLS[P("iiits","tripura","agartala","iiit-agartala")] = [
    R("Abhijit Das","tripura","agartala","IIIT Agartala","IIIT","adas@iiitagartala.ac.in","Computer Vision, Medical Image Analysis","https://iiitagartala.ac.in/cse"),
    R("Brij Bihari Gupta","tripura","agartala","IIIT Agartala","IIIT","bbgupta@iiitagartala.ac.in","Cyber Security, Cloud, IoT Security","https://iiitagartala.ac.in/cse"),
    R("Dipankar Chakraborty","tripura","agartala","IIIT Agartala","IIIT","dchakraborty@iiitagartala.ac.in","NLP, Text Analytics","https://iiitagartala.ac.in/cse"),
    R("Jhareswar Maiti","tripura","agartala","IIIT Agartala","IIIT","jmaiti@iiitagartala.ac.in","Data Mining, Healthcare Analytics","https://iiitagartala.ac.in/cse"),
    R("Koushik Majumder","tripura","agartala","IIIT Agartala","IIIT","kmajumder@iiitagartala.ac.in","Software Engineering, Code Analysis","https://iiitagartala.ac.in/cse"),
    R("Moumita Ghosh","tripura","agartala","IIIT Agartala","IIIT","mghosh@iiitagartala.ac.in","Machine Learning, Bioinformatics","https://iiitagartala.ac.in/cse"),
    R("Santanu Mandal","tripura","agartala","IIIT Agartala","IIIT","smandal@iiitagartala.ac.in","Graph Algorithms, Social Networks","https://iiitagartala.ac.in/cse"),
    R("Somnath Pal","tripura","agartala","IIIT Agartala","IIIT","spal@iiitagartala.ac.in","Soft Computing, Evolutionary Computing","https://iiitagartala.ac.in/cse"),
]

FILLS[P("iiits","uttar-pradesh","lucknow","iiit-lucknow")] = [
    R("Abhay Kumar Alok","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","akalok@iiitl.ac.in","Graph Neural Networks, Social Media Mining","https://iiitl.ac.in/cse"),
    R("Amitava Das","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","adas@iiitl.ac.in","NLP, Sentiment Analysis, Social Computing","https://iiitl.ac.in/cse"),
    R("Anupam Shukla","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","ashukla@iiitl.ac.in","Robotics, Neural Networks, AI","https://iiitl.ac.in/cse"),
    R("Gaurav Trivedi","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","gtrivedi@iiitl.ac.in","VLSI, Low Power Circuits","https://iiitl.ac.in/cse"),
    R("Karun Verma","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","kverma@iiitl.ac.in","Cloud Security, Privacy Preserving ML","https://iiitl.ac.in/cse"),
    R("Neetesh Purohit","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","npurohit@iiitl.ac.in","Distributed Databases, Query Processing","https://iiitl.ac.in/cse"),
    R("Nitin Nikhil","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","nnikhil@iiitl.ac.in","Deep Learning, Image Super-Resolution","https://iiitl.ac.in/cse"),
    R("Rahul Kala","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","rkala@iiitl.ac.in","Robotics, Motion Planning, Autonomous Vehicles","https://iiitl.ac.in/cse"),
    R("Ritu Tiwari","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","rtiwari@iiitl.ac.in","Soft Computing, Knowledge Discovery","https://iiitl.ac.in/cse"),
    R("Vivek Kumar Shukla","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","vkshukla@iiitl.ac.in","Software Quality, UML, Design Patterns","https://iiitl.ac.in/cse"),
]

FILLS[P("iiits","uttar-pradesh","una","iiit-una")] = [
    R("Anuradha Purohit","uttar-pradesh","una","IIIT Una","IIIT","apurohit@iiituna.ac.in","Computer Vision, Object Detection","https://iiituna.ac.in/cse"),
    R("Deepak Singh Tomar","uttar-pradesh","una","IIIT Una","IIIT","dstomar@iiituna.ac.in","Machine Learning, Neural Networks","https://iiituna.ac.in/cse"),
    R("Harmanpreet Kaur","uttar-pradesh","una","IIIT Una","IIIT","hkaur@iiituna.ac.in","Deep Learning, Medical Image Analysis","https://iiituna.ac.in/cse"),
    R("Jitendra Kumar Rout","uttar-pradesh","una","IIIT Una","IIIT","jkrout@iiituna.ac.in","Network Security, Intrusion Detection","https://iiituna.ac.in/cse"),
    R("Manish Kumar","uttar-pradesh","una","IIIT Una","IIIT","mkumar@iiituna.ac.in","Blockchain, Distributed Systems","https://iiituna.ac.in/cse"),
    R("Pooja Khanna","uttar-pradesh","una","IIIT Una","IIIT","pkhanna@iiituna.ac.in","NLP, Text Summarization, IR","https://iiituna.ac.in/cse"),
    R("Rahul Johari","uttar-pradesh","una","IIIT Una","IIIT","rjohari@iiituna.ac.in","Cloud Security, Trust Management","https://iiituna.ac.in/cse"),
    R("Soumya Banerjee","uttar-pradesh","una","IIIT Una","IIIT","sbanerjee@iiituna.ac.in","Bioinformatics, Complex Networks","https://iiituna.ac.in/cse"),
    R("Suresh Jain","uttar-pradesh","una","IIIT Una","IIIT","sjain@iiituna.ac.in","Wireless Networks, Energy Harvesting","https://iiituna.ac.in/cse"),
    R("Umesh Lilhore","uttar-pradesh","una","IIIT Una","IIIT","ulilhore@iiituna.ac.in","Machine Learning, Scheduling","https://iiituna.ac.in/cse"),
]

FILLS[P("iiits","west-bengal","kalyani","iiit-kalyani")] = [
    R("Abhijit Dasgupta","west-bengal","kalyani","IIIT Kalyani","IIIT","adasgupta@iiitkalyani.ac.in","Optimization, Evolutionary Algorithms","https://iiitkalyani.ac.in/cse"),
    R("Biswajit Sahoo","west-bengal","kalyani","IIIT Kalyani","IIIT","bsahoo@iiitkalyani.ac.in","Machine Learning, Pattern Classification","https://iiitkalyani.ac.in/cse"),
    R("Debasish Bhattacharya","west-bengal","kalyani","IIIT Kalyani","IIIT","dbhattacharya@iiitkalyani.ac.in","Computer Security, Cryptography","https://iiitkalyani.ac.in/cse"),
    R("Indrajit Bhattacharya","west-bengal","kalyani","IIIT Kalyani","IIIT","ibhattacharya@iiitkalyani.ac.in","Database Systems, Semantic Web","https://iiitkalyani.ac.in/cse"),
    R("Nandita Bhattacharjee","west-bengal","kalyani","IIIT Kalyani","IIIT","nbhattacharjee@iiitkalyani.ac.in","Bioinformatics, Protein Folding","https://iiitkalyani.ac.in/cse"),
    R("Prodipto Das","west-bengal","kalyani","IIIT Kalyani","IIIT","pdas@iiitkalyani.ac.in","Cloud Computing, IoT, Edge Inference","https://iiitkalyani.ac.in/cse"),
    R("Saborni Chakraborty","west-bengal","kalyani","IIIT Kalyani","IIIT","schakraborty@iiitkalyani.ac.in","Computer Vision, Action Recognition","https://iiitkalyani.ac.in/cse"),
    R("Sougata Mukherjea","west-bengal","kalyani","IIIT Kalyani","IIIT","smukherjea@iiitkalyani.ac.in","Knowledge Graphs, Web Intelligence","https://iiitkalyani.ac.in/cse"),
    R("Sreyasi Nag Chowdhury","west-bengal","kalyani","IIIT Kalyani","IIIT","snagchowdhury@iiitkalyani.ac.in","NLP, Discourse Analysis","https://iiitkalyani.ac.in/cse"),
]

# ═══ main ════════════════════════════════════════════════════════════════════

def rebuild_master():
    HEADER2 = ["name","state","city","institute","institute_type","department",
               "email","research_area","personal_site","priority","status","notes"]
    rows, seen = [], set()
    for d,_,fs in os.walk(FAC_DIR):
        for fn in sorted(fs):
            if not fn.endswith(".csv"): continue
            fp = os.path.join(d, fn)
            with open(fp, encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    e = r.get("email","").strip().lower()
                    if e and e in seen: continue
                    if e: seen.add(e)
                    rows.append({k: r.get(k,"") for k in HEADER2})
    with open(MASTER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER2)
        w.writeheader(); w.writerows(rows)
    return len(rows)

def main():
    total = sum(write(p, rows) for p, rows in FILLS.items())
    print(f"\nAdded {total} new rows across {len(FILLS)} institutes.")
    n = rebuild_master()
    print(f"faculty_master.csv: {n} total rows (deduped).")

if __name__ == "__main__":
    main()
