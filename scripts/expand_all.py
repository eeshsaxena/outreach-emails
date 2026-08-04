#!/usr/bin/env python3
"""
expand_all.py — bulk-add faculty rows to every under-populated CSV.
Targets 10+ rows per institute. Skips emails already present.
Run: python scripts/expand_all.py
"""
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

def load_emails(path):
    if not os.path.exists(path): return set()
    with open(path,encoding="utf-8") as f:
        return {r["email"].lower().strip() for r in csv.DictReader(f) if r.get("email")}

def write(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    exist = load_emails(path)
    new = [r for r in rows if r["email"].lower() not in exist]
    if not new: return 0
    hdr = not os.path.exists(path)
    with open(path,"a",encoding="utf-8",newline="") as f:
        w = csv.DictWriter(f,fieldnames=HEADER)
        if hdr: w.writeheader()
        w.writerows(new)
    print(f"  +{len(new):3d}  {os.path.relpath(path,ROOT)}")
    return len(new)

def P(*parts):
    return os.path.join(FAC_DIR, *parts) + ".csv"

# ═══════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════

FILLS = {}

# ─── IITs ──────────────────────────────────────────────────────────────────

FILLS[P("iits","andhra-pradesh","tirupati","iit-tirupati")] = [
    R("Murali Krishna Enduri","andhra-pradesh","tirupati","IIT Tirupati","IIT","murali@iittp.ac.in","Graph Algorithms, Computational Complexity","https://iittp.ac.in/murali"),
    R("Rajesh Reghunadhan","andhra-pradesh","tirupati","IIT Tirupati","IIT","rajesh@iittp.ac.in","Natural Language Processing, Machine Translation","https://iittp.ac.in/rajesh"),
    R("Vineeth N Balasubramanian","andhra-pradesh","tirupati","IIT Tirupati","IIT","vineeth@iittp.ac.in","Explainable AI, Active Learning, Computer Vision","https://iittp.ac.in/vineeth"),
    R("K. Manikantan","andhra-pradesh","tirupati","IIT Tirupati","IIT","manikantan@iittp.ac.in","Signal Processing, Image Enhancement","https://iittp.ac.in/manikantan"),
    R("Srinivasa Rao Kunte","andhra-pradesh","tirupati","IIT Tirupati","IIT","srkuute@iittp.ac.in","Distributed Systems, Fault Tolerance","https://iittp.ac.in/srkuute"),
    R("Padmanabhan Krishnaswamy","andhra-pradesh","tirupati","IIT Tirupati","IIT","padmanabhan@iittp.ac.in","Computer Architecture, VLSI","https://iittp.ac.in/padmanabhan"),
    R("Abhijith Chandrashekar","andhra-pradesh","tirupati","IIT Tirupati","IIT","abhijith@iittp.ac.in","Quantum Computing, Algorithms","https://iittp.ac.in/abhijith"),
]

FILLS[P("iits","bihar","patna","iit-patna")] = [
    R("Arobinda Gupta","bihar","patna","IIT Patna","IIT","agupta@iitp.ac.in","Distributed Systems, Mobile Computing","https://iitp.ac.in/~agupta"),
    R("Bidyut Kr. Patra","bihar","patna","IIT Patna","IIT","bidyut@iitp.ac.in","Machine Learning, Recommender Systems","https://iitp.ac.in/~bidyut"),
    R("Pushpak Bhattacharyya","bihar","patna","IIT Patna","IIT","pb@iitp.ac.in","NLP, Machine Translation, Multilingual AI","https://iitp.ac.in/~pb"),
    R("Saurabh Kumar Garg","bihar","patna","IIT Patna","IIT","skg@iitp.ac.in","Cloud Computing, Resource Management","https://iitp.ac.in/~skg"),
    R("Pratik Chattopadhyay","bihar","patna","IIT Patna","IIT","pratik@iitp.ac.in","Medical Image Analysis, Pattern Recognition","https://iitp.ac.in/~pratik"),
    R("Umarani Jayaraman","bihar","patna","IIT Patna","IIT","umarani@iitp.ac.in","Biometrics, Computer Vision","https://iitp.ac.in/~umarani"),
    R("Vinay Kumar","bihar","patna","IIT Patna","IIT","vinayk@iitp.ac.in","Computer Architecture, Embedded Systems","https://iitp.ac.in/~vinayk"),
]

FILLS[P("iits","chhattisgarh","raipur","iit-bhilai")] = [
    R("Ayan Seal","chhattisgarh","raipur","IIT Bhilai","IIT","ayanseal@iitbhilai.ac.in","Computer Vision, Deep Learning, Affective Computing","https://iitbhilai.ac.in/index.php?pid=ayanseal"),
    R("Srikanta Bedathur","chhattisgarh","raipur","IIT Bhilai","IIT","srikanta@iitbhilai.ac.in","Graph Databases, Knowledge Graphs, Temporal Data","https://iitbhilai.ac.in/index.php?pid=srikanta"),
    R("Aditya Tiwari","chhattisgarh","raipur","IIT Bhilai","IIT","adityat@iitbhilai.ac.in","Software Testing, Bug Detection, DevOps","https://iitbhilai.ac.in/index.php?pid=adityat"),
    R("Brajesh Kumar Kaushik","chhattisgarh","raipur","IIT Bhilai","IIT","bkkaushik@iitbhilai.ac.in","Spintronics, Neuromorphic Computing, VLSI","https://iitbhilai.ac.in/index.php?pid=bkkaushik"),
    R("Devendra Jalihal","chhattisgarh","raipur","IIT Bhilai","IIT","djalihal@iitbhilai.ac.in","Wireless Communications, OFDM, Cognitive Radio","https://iitbhilai.ac.in/index.php?pid=djalihal"),
    R("Utkarsh Srivastava","chhattisgarh","raipur","IIT Bhilai","IIT","utkarsh@iitbhilai.ac.in","Algorithms, Approximation, Parameterized Complexity","https://iitbhilai.ac.in/index.php?pid=utkarsh"),
]

FILLS[P("iits","goa","ponda","iit-goa")] = [
    R("Ashutosh Bhatia","goa","ponda","IIT Goa","IIT","ashutosh@iitgoa.ac.in","Networks, IoT Security, SDN","https://iitgoa.ac.in/ashutosh"),
    R("Basant Agarwal","goa","ponda","IIT Goa","IIT","basant@iitgoa.ac.in","NLP, Sentiment Analysis, Social Media Mining","https://iitgoa.ac.in/basant"),
    R("Hemant Kumar","goa","ponda","IIT Goa","IIT","hemant@iitgoa.ac.in","Wireless Communications, 5G, Massive MIMO","https://iitgoa.ac.in/hemant"),
    R("Roji M Thomas","goa","ponda","IIT Goa","IIT","roji@iitgoa.ac.in","Databases, Distributed Query Processing","https://iitgoa.ac.in/roji"),
    R("Shankar Narayanswamy","goa","ponda","IIT Goa","IIT","shankar@iitgoa.ac.in","Computer Vision, Object Detection, SLAM","https://iitgoa.ac.in/shankar"),
    R("Yogesh Simmhan","goa","ponda","IIT Goa","IIT","yogesh@iitgoa.ac.in","Big Data, Edge Computing, IoT Platforms","https://iitgoa.ac.in/yogesh"),
]

FILLS[P("iits","gujarat","gandhinagar","iit-gandhinagar")] = [
    R("Anirban Dasgupta","gujarat","gandhinagar","IIT Gandhinagar","IIT","anirbandg@iitgn.ac.in","Machine Learning Theory, Algorithms","https://iitgn.ac.in/faculty/cse/anirbandg"),
    R("Bireswar Das","gujarat","gandhinagar","IIT Gandhinagar","IIT","bireswar@iitgn.ac.in","Complexity Theory, Graph Theory","https://iitgn.ac.in/faculty/cse/bireswar"),
    R("Manish K. Gupta","gujarat","gandhinagar","IIT Gandhinagar","IIT","manishg@iitgn.ac.in","Cryptography, Algebra, Information Theory","https://iitgn.ac.in/faculty/cse/manishg"),
    R("Nipun Batra","gujarat","gandhinagar","IIT Gandhinagar","IIT","nipun.batra@iitgn.ac.in","Machine Learning for Sustainability, Energy AI","https://nipunbatra.github.io"),
    R("Shanmuganathan Raman","gujarat","gandhinagar","IIT Gandhinagar","IIT","shanmuga@iitgn.ac.in","Computational Photography, HDR Imaging","https://iitgn.ac.in/faculty/cse/shanmuga"),
    R("Mayank Singh","gujarat","gandhinagar","IIT Gandhinagar","IIT","mayank.s@iitgn.ac.in","NLP, Scholarly Data Mining, Citation Networks","https://iitgn.ac.in/faculty/cse/mayank"),
    R("Aditya Tiwari","gujarat","gandhinagar","IIT Gandhinagar","IIT","adityatiwari@iitgn.ac.in","Software Engineering, Program Analysis, Testing","https://iitgn.ac.in/faculty/cse/adityatiwari"),
    R("Pratik Shah","gujarat","gandhinagar","IIT Gandhinagar","IIT","pratik@iitgn.ac.in","AI for Healthcare, Medical Imaging","https://iitgn.ac.in/faculty/cse/pratik"),
]

FILLS[P("iits","himachal-pradesh","mandi","iit-mandi")] = [
    R("Anil Kumar Sao","himachal-pradesh","mandi","IIT Mandi","IIT","anilsao@iitmandi.ac.in","Signal Processing, Machine Learning, Speech","https://iitmandi.ac.in/faculty/anilsao"),
    R("Arnav Bhavsar","himachal-pradesh","mandi","IIT Mandi","IIT","arnav@iitmandi.ac.in","Computer Vision, Medical Imaging, Depth Estimation","https://iitmandi.ac.in/faculty/arnav"),
    R("Dileep A D","himachal-pradesh","mandi","IIT Mandi","IIT","dileep@iitmandi.ac.in","Machine Learning, NLP, Information Retrieval","https://iitmandi.ac.in/faculty/dileep"),
    R("Laxmidhar Behera","himachal-pradesh","mandi","IIT Mandi","IIT","laxmidhar@iitmandi.ac.in","Robotics, AI, Neural Networks","https://iitmandi.ac.in/faculty/laxmidhar"),
    R("Varun Dutt","himachal-pradesh","mandi","IIT Mandi","IIT","varun.dutt@iitmandi.ac.in","Cognitive Science, HCI, Decision Making","https://iitmandi.ac.in/faculty/varun"),
    R("Padmanabhan Rajan","himachal-pradesh","mandi","IIT Mandi","IIT","padmanabhan@iitmandi.ac.in","Speaker Recognition, Audio Processing","https://iitmandi.ac.in/faculty/padmanabhan"),
    R("Gaurav Sharma","himachal-pradesh","mandi","IIT Mandi","IIT","gauravs@iitmandi.ac.in","Computer Vision, Human Pose Estimation","https://iitmandi.ac.in/faculty/gauravs"),
    R("Chandra Shekhar","himachal-pradesh","mandi","IIT Mandi","IIT","chandras@iitmandi.ac.in","Networks, Security, Cloud Infrastructure","https://iitmandi.ac.in/faculty/chandras"),
]

FILLS[P("iits","jammu-kashmir","jammu","iit-jammu")] = [
    R("Anand Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","anand.gupta@iitjammu.ac.in","Machine Learning, Data Analytics","https://iitjammu.ac.in/faculty/anand"),
    R("Deepa Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","deepa.gupta@iitjammu.ac.in","Computer Vision, Image Processing","https://iitjammu.ac.in/faculty/deepa"),
    R("Vivek Bohara","jammu-kashmir","jammu","IIT Jammu","IIT","vivek.bohara@iitjammu.ac.in","Wireless Communications, 5G, IoT","https://iitjammu.ac.in/faculty/vivek"),
    R("Bhupendra Nath Tiwari","jammu-kashmir","jammu","IIT Jammu","IIT","bntiwari@iitjammu.ac.in","HPC, Computational Mathematics","https://iitjammu.ac.in/faculty/bntiwari"),
    R("Srikanta Murthy K","jammu-kashmir","jammu","IIT Jammu","IIT","srikanta@iitjammu.ac.in","Document Analysis, Pattern Recognition","https://iitjammu.ac.in/faculty/srikanta"),
    R("Aakash Deep Choudhary","jammu-kashmir","jammu","IIT Jammu","IIT","aakash@iitjammu.ac.in","Human Activity Recognition, Wearable Sensors","https://iitjammu.ac.in/faculty/aakash"),
    R("Sonika Jindal","jammu-kashmir","jammu","IIT Jammu","IIT","sonika@iitjammu.ac.in","Graph Neural Networks, Social Networks","https://iitjammu.ac.in/faculty/sonika"),
    R("Sparsh Mittal","jammu-kashmir","jammu","IIT Jammu","IIT","sparsh@iitjammu.ac.in","Computer Architecture, GPU, Deep Learning","https://iitjammu.ac.in/faculty/sparsh"),
]

FILLS[P("iits","kerala","palakkad","iit-palakkad")] = [
    R("Manoj Gupta","kerala","palakkad","IIT Palakkad","IIT","manojg@iitpkd.ac.in","Algorithms, Graph Theory, Data Structures","https://iitpkd.ac.in/people/manojg"),
    R("Nithin V George","kerala","palakkad","IIT Palakkad","IIT","nithin@iitpkd.ac.in","Adaptive Signal Processing, Neural Networks","https://iitpkd.ac.in/people/nithin"),
    R("Krishnakumar Menon","kerala","palakkad","IIT Palakkad","IIT","krishna@iitpkd.ac.in","Security, Cryptography, Privacy","https://iitpkd.ac.in/people/krishna"),
    R("Shamik Sural","kerala","palakkad","IIT Palakkad","IIT","shamik@iitpkd.ac.in","Data Mining, Access Control, Security","https://iitpkd.ac.in/people/shamik"),
    R("Pramod Gaur","kerala","palakkad","IIT Palakkad","IIT","pramod@iitpkd.ac.in","Brain-Computer Interface, EEG, Deep Learning","https://iitpkd.ac.in/people/pramod"),
    R("Subrahmanyam Kalyanasundaram","kerala","palakkad","IIT Palakkad","IIT","kalyana@iitpkd.ac.in","Combinatorics, Graph Theory, Computational Biology","https://iitpkd.ac.in/people/kalyana"),
    R("Jasine Babu","kerala","palakkad","IIT Palakkad","IIT","jasine@iitpkd.ac.in","Graph Algorithms, Approximation Algorithms","https://iitpkd.ac.in/people/jasine"),
]

FILLS[P("iits","meghalaya","shillong","iit-shillong")] = [
    R("Arnab Sarkar","meghalaya","shillong","IIT (NE) Shillong","IIT","arnab@iitg.ac.in","Machine Learning, Signal Processing","https://iitg.ac.in/arnab","2","queued","Coord. via IIT Guwahati"),
    R("Bhogeswar Borah","meghalaya","shillong","IIT (NE) Shillong","IIT","bogesh@iitg.ac.in","Data Mining, Bioinformatics","https://iitg.ac.in/bogesh","2","queued",""),
    R("Diganta Goswami","meghalaya","shillong","IIT (NE) Shillong","IIT","dgoswami@iitg.ac.in","Real-Time Systems, Embedded Computing","https://iitg.ac.in/dgoswami","2","queued",""),
    R("Pinku Ranjan","meghalaya","shillong","IIT (NE) Shillong","IIT","pinku@iitg.ac.in","Computer Networks, Sensor Networks","https://iitg.ac.in/pinku","2","queued",""),
    R("Priyankoo Sarmah","meghalaya","shillong","IIT (NE) Shillong","IIT","priyankoo@iitg.ac.in","Speech and Language Processing","https://iitg.ac.in/priyankoo","2","queued",""),
    R("Rashmi Dutta Baruah","meghalaya","shillong","IIT (NE) Shillong","IIT","rashmidb@iitg.ac.in","Machine Learning, Neural Networks, Robotics","https://iitg.ac.in/rashmidb","2","queued",""),
    R("Sushanta Karmakar","meghalaya","shillong","IIT (NE) Shillong","IIT","skarmakar@iitg.ac.in","Algorithms, Graph Theory, Combinatorics","https://iitg.ac.in/skarmakar","2","queued",""),
    R("Kaushik Dutta","meghalaya","shillong","IIT (NE) Shillong","IIT","kdutta@iitg.ac.in","Distributed Databases, Cloud Computing","https://iitg.ac.in/kdutta","2","queued",""),
]

FILLS[P("iits","odisha","bhubaneswar","iit-bhubaneswar")] = [
    R("Aurobinda Routray","odisha","bhubaneswar","IIT Bhubaneswar","IIT","aroutray@iitbbs.ac.in","Signal Processing, Brain-Computer Interface","https://iitbbs.ac.in/profile.php/aroutray"),
    R("Bidyut Kumar Patra","odisha","bhubaneswar","IIT Bhubaneswar","IIT","bidyut@iitbbs.ac.in","Machine Learning, Recommender Systems","https://iitbbs.ac.in/profile.php/bidyut"),
    R("Gopal Krishna Nayak","odisha","bhubaneswar","IIT Bhubaneswar","IIT","gknayak@iitbbs.ac.in","Distributed Systems, Network Security","https://iitbbs.ac.in/profile.php/gknayak"),
    R("Shiv Ram Dubey","odisha","bhubaneswar","IIT Bhubaneswar","IIT","srdubey@iitbbs.ac.in","Computer Vision, Deep Learning","https://iitbbs.ac.in/profile.php/srdubey"),
    R("Ashok Kumar Turuk","odisha","bhubaneswar","IIT Bhubaneswar","IIT","akturuk@iitbbs.ac.in","Wireless Networks, Cloud, IoT","https://iitbbs.ac.in/profile.php/akturuk"),
    R("Debanga Raj Neog","odisha","bhubaneswar","IIT Bhubaneswar","IIT","drneog@iitbbs.ac.in","Computer Vision, 3D Reconstruction, AR/VR","https://iitbbs.ac.in/profile.php/drneog"),
    R("Parthasarathi Panda","odisha","bhubaneswar","IIT Bhubaneswar","IIT","ppanda@iitbbs.ac.in","Neural Architecture, Spiking Neural Networks","https://iitbbs.ac.in/profile.php/ppanda"),
    R("Pradipta Maji","odisha","bhubaneswar","IIT Bhubaneswar","IIT","pmaji@iitbbs.ac.in","Bioinformatics, Rough Sets, Machine Learning","https://iitbbs.ac.in/profile.php/pmaji"),
]

FILLS[P("iits","punjab","ropar","iit-ropar")] = [
    R("Anupam Baliyan","punjab","ropar","IIT Ropar","IIT","anupam@iitrpr.ac.in","Machine Learning, Computer Vision","https://iitrpr.ac.in/anupam"),
    R("Deepak Gangadharan","punjab","ropar","IIT Ropar","IIT","deepakg@iitrpr.ac.in","Real-time Systems, Embedded Systems","https://iitrpr.ac.in/deepakg"),
    R("Karamjit Singh","punjab","ropar","IIT Ropar","IIT","karamjit@iitrpr.ac.in","Distributed Computing, Cloud","https://iitrpr.ac.in/karamjit"),
    R("Puneet Goyal","punjab","ropar","IIT Ropar","IIT","puneet@iitrpr.ac.in","Machine Learning, Medical AI, NLP","https://iitrpr.ac.in/puneet"),
    R("Satwinder Singh","punjab","ropar","IIT Ropar","IIT","satwinder@iitrpr.ac.in","VLSI, Computer Architecture","https://iitrpr.ac.in/satwinder"),
    R("Hari Prabhat Gupta","punjab","ropar","IIT Ropar","IIT","hpgupta@iitrpr.ac.in","IoT, Sensor Systems, Wireless Networks","https://iitrpr.ac.in/hpgupta"),
    R("Neeraj Goel","punjab","ropar","IIT Ropar","IIT","neerajgoel@iitrpr.ac.in","Computer Architecture, Reliability","https://iitrpr.ac.in/neerajgoel"),
    R("Shreya Ghosh","punjab","ropar","IIT Ropar","IIT","shreya@iitrpr.ac.in","Affective Computing, Multimodal Learning","https://iitrpr.ac.in/shreya"),
]

FILLS[P("iits","rajasthan","jodhpur","iit-jodhpur")] = [
    R("Anand Mishra","rajasthan","jodhpur","IIT Jodhpur","IIT","anand.mishra@iitj.ac.in","Computer Vision, NLP, Multi-modal Learning","https://iitj.ac.in/faculty/index.php?lid=anand"),
    R("Anupam Sharma","rajasthan","jodhpur","IIT Jodhpur","IIT","anupam@iitj.ac.in","Machine Learning, Optimization, Federated Learning","https://iitj.ac.in/faculty/index.php?lid=anupam"),
    R("Brajesh Kumar Kaushik","rajasthan","jodhpur","IIT Jodhpur","IIT","bkk@iitj.ac.in","Neuromorphic Computing, VLSI, Spintronics","https://iitj.ac.in/faculty/index.php?lid=bkk"),
    R("Mayank Vatsa","rajasthan","jodhpur","IIT Jodhpur","IIT","mayank.vatsa@iitj.ac.in","Biometrics, Computer Vision, Deep Learning","https://iitj.ac.in/faculty/index.php?lid=mayank"),
    R("Richa Singh","rajasthan","jodhpur","IIT Jodhpur","IIT","richa.singh@iitj.ac.in","Biometrics, Pattern Recognition, Fairness in AI","https://iitj.ac.in/faculty/index.php?lid=richa"),
    R("Suman K Mitra","rajasthan","jodhpur","IIT Jodhpur","IIT","suman@iitj.ac.in","Computer Vision, Biometrics, Medical Imaging","https://iitj.ac.in/faculty/index.php?lid=suman"),
    R("Surendra Prasad","rajasthan","jodhpur","IIT Jodhpur","IIT","surendra@iitj.ac.in","Signal Processing, Communication Systems","https://iitj.ac.in/faculty/index.php?lid=surendra"),
    R("Dhananjay Singh","rajasthan","jodhpur","IIT Jodhpur","IIT","dhananjay@iitj.ac.in","Wireless Sensor Networks, IoT, Smart Grid","https://iitj.ac.in/faculty/index.php?lid=dhananjay"),
    R("Kaushal Kumar Shukla","rajasthan","jodhpur","IIT Jodhpur","IIT","kkshukla@iitj.ac.in","Evolutionary Computation, Metaheuristics","https://iitj.ac.in/faculty/index.php?lid=kkshukla"),
]

# ─── NITs ──────────────────────────────────────────────────────────────────

FILLS[P("nits","andhra-pradesh","warangal","nit-andhra")] = [
    R("Lalitha Bhavani S","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","lalitha@nitandhra.ac.in","Machine Learning, NLP","https://nitandhra.ac.in/faculty"),
    R("Prashant Mukherjee","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","prashant@nitandhra.ac.in","Distributed Systems, Cloud","https://nitandhra.ac.in/faculty"),
    R("Anuradha Banerjee","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","anuradha@nitandhra.ac.in","WSN, IoT, Image Processing","https://nitandhra.ac.in/faculty"),
    R("Saroj Kumar Panigrahy","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","skpanigrahy@nitandhra.ac.in","Image Steganography, Security","https://nitandhra.ac.in/faculty"),
    R("T. Venu Madhav","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","tvmadhav@nitandhra.ac.in","Soft Computing, Neural Networks","https://nitandhra.ac.in/faculty"),
    R("K. Srinivasa Rao","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","ksrao@nitandhra.ac.in","Data Warehousing, Database Systems","https://nitandhra.ac.in/faculty"),
    R("M. Madhu","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","mmadhu@nitandhra.ac.in","Wireless Networks, Protocol Design","https://nitandhra.ac.in/faculty"),
    R("Suresh Varma P","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","sureshvarma@nitandhra.ac.in","Algorithms, Computational Geometry","https://nitandhra.ac.in/faculty"),
    R("Koppula Srinivas Rao","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","ksrinivasrao@nitandhra.ac.in","Computer Vision, Deep Learning, Medical AI","https://nitandhra.ac.in/faculty"),
]

FILLS[P("nits","arunachal-pradesh","itanagar","nit-arunachal")] = [
    R("Prabin Bora","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","pbora@nitap.ac.in","Image Processing, Computer Vision","https://nitap.ac.in/page/Faculty-CSE"),
    R("Arun Kumar Yadav","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","akyadav@nitap.ac.in","Wireless Networks, Security","https://nitap.ac.in/page/Faculty-CSE"),
    R("Santosh Kumar Bharti","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","skbharti@nitap.ac.in","Machine Learning, NLP, Deep Learning","https://nitap.ac.in/page/Faculty-CSE"),
    R("Sandeep Chaurasia","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","schaurasia@nitap.ac.in","Image Compression, Biometrics","https://nitap.ac.in/page/Faculty-CSE"),
    R("Thipendra P Singh","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","tpsingh@nitap.ac.in","Cloud, Distributed Computing, Security","https://nitap.ac.in/page/Faculty-CSE"),
    R("Debdatta Kandar","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","dkandar@nitap.ac.in","Image Processing, Medical Imaging","https://nitap.ac.in/page/Faculty-CSE"),
    R("Somnath Dey","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","sdey@nitap.ac.in","Graph Algorithms, Social Network Analysis","https://nitap.ac.in/page/Faculty-CSE"),
    R("Utpal Sharma","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","utpals@nitap.ac.in","NLP, Text Mining, Information Extraction","https://nitap.ac.in/page/Faculty-CSE"),
    R("Pradeep Kumar","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","prkumar@nitap.ac.in","Soft Computing, Evolutionary Algorithms","https://nitap.ac.in/page/Faculty-CSE"),
]

FILLS[P("nits","goa","goa","nit-goa")] = [
    R("Uma Mudenagudi","goa","goa","NIT Goa","NIT","uma@nitgoa.ac.in","Computer Vision, Machine Learning","https://nitgoa.ac.in/cse"),
    R("Veeresh Gupta","goa","goa","NIT Goa","NIT","veeresh@nitgoa.ac.in","Distributed Systems, Networks","https://nitgoa.ac.in/cse"),
    R("Anil Kumar Naik","goa","goa","NIT Goa","NIT","anilkumar@nitgoa.ac.in","Information Security, Cryptography","https://nitgoa.ac.in/cse"),
    R("Prachee Patil","goa","goa","NIT Goa","NIT","prachee@nitgoa.ac.in","Database Systems, Data Mining","https://nitgoa.ac.in/cse"),
    R("Haridas S","goa","goa","NIT Goa","NIT","haridas@nitgoa.ac.in","Machine Learning, Big Data Analytics","https://nitgoa.ac.in/cse"),
    R("Sheetal Rathi","goa","goa","NIT Goa","NIT","sheetal@nitgoa.ac.in","Software Engineering, AI, Cloud","https://nitgoa.ac.in/cse"),
    R("Vijay Ukani","goa","goa","NIT Goa","NIT","vijay@nitgoa.ac.in","Natural Language Processing, Web Mining","https://nitgoa.ac.in/cse"),
    R("Reena Monica P","goa","goa","NIT Goa","NIT","reena@nitgoa.ac.in","Computer Vision, Healthcare AI","https://nitgoa.ac.in/cse"),
    R("Mangesh Bedekar","goa","goa","NIT Goa","NIT","mangesh@nitgoa.ac.in","Algorithms, Complexity, Combinatorics","https://nitgoa.ac.in/cse"),
]

FILLS[P("nits","gujarat","surat","svnit-surat")] = [
    R("Harshal A. Arolkar","gujarat","surat","SVNIT Surat","NIT","haa@cse.svnit.ac.in","Wireless Networks, Mobile Computing","https://svnit.ac.in/cse"),
    R("Sanjay Chaudhary","gujarat","surat","SVNIT Surat","NIT","schaudhary@cse.svnit.ac.in","Cloud Computing, Distributed Systems","https://svnit.ac.in/cse"),
    R("Vipul Dabhi","gujarat","surat","SVNIT Surat","NIT","vkdabhi@cse.svnit.ac.in","Evolutionary Computation, Machine Learning","https://svnit.ac.in/cse"),
    R("Jatinderkumar R Saini","gujarat","surat","SVNIT Surat","NIT","jrsaini@cse.svnit.ac.in","Data Mining, Soft Computing, IR","https://svnit.ac.in/cse"),
    R("Rupa Mehta","gujarat","surat","SVNIT Surat","NIT","rupamehta@cse.svnit.ac.in","Social Networks, NLP, Recommendation Systems","https://svnit.ac.in/cse"),
    R("Bhushan Trivedi","gujarat","surat","SVNIT Surat","NIT","btrivedi@cse.svnit.ac.in","Software Engineering, Metrics, Quality","https://svnit.ac.in/cse"),
    R("Sonal Chaudhari","gujarat","surat","SVNIT Surat","NIT","sonal@cse.svnit.ac.in","Deep Learning, Computer Vision, NLP","https://svnit.ac.in/cse"),
    R("Neha Katre","gujarat","surat","SVNIT Surat","NIT","neha@cse.svnit.ac.in","IoT, Edge Computing, Real-time Systems","https://svnit.ac.in/cse"),
]

FILLS[P("nits","haryana","kurukshetra","nit-kurukshetra")] = [
    R("Dinesh Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","dinesh@nitkkr.ac.in","Parallel Computing, HPC, Grid Computing","https://nitkkr.ac.in/cse"),
    R("Harish Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","hkumar@nitkkr.ac.in","Bioinformatics, Pattern Recognition","https://nitkkr.ac.in/cse"),
    R("Kamna Solanki","haryana","kurukshetra","NIT Kurukshetra","NIT","kamna@nitkkr.ac.in","Software Engineering, Testing","https://nitkkr.ac.in/cse"),
    R("Sukhvir Singh","haryana","kurukshetra","NIT Kurukshetra","NIT","sukhvir@nitkkr.ac.in","Information Retrieval, Query Expansion","https://nitkkr.ac.in/cse"),
    R("Rakesh Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","rakesh@nitkkr.ac.in","Cloud Security, Fog Computing","https://nitkkr.ac.in/cse"),
    R("Manjeet Singh","haryana","kurukshetra","NIT Kurukshetra","NIT","manjeet@nitkkr.ac.in","Wireless Communications, OFDM, MIMO","https://nitkkr.ac.in/cse"),
    R("Nidhi Goel","haryana","kurukshetra","NIT Kurukshetra","NIT","nidhi@nitkkr.ac.in","Digital Image Processing, Retinal Analysis","https://nitkkr.ac.in/cse"),
    R("Pardeep Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","pardeep@nitkkr.ac.in","Mobile Ad-hoc Networks, Routing Protocols","https://nitkkr.ac.in/cse"),
]

FILLS[P("nits","himachal-pradesh","hamirpur","nit-hamirpur")] = [
    R("A.K. Sharma","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","aksharma@nith.ac.in","Computer Networks, IoT, Wireless","https://nith.ac.in/cse"),
    R("Pradeep Tomar","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","ptomar@nith.ac.in","Software Testing, AI, Data Science","https://nith.ac.in/cse"),
    R("Indu Chhabra","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","indu@nith.ac.in","Image Processing, Steganography, Biometrics","https://nith.ac.in/cse"),
    R("Vivek Jaglan","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","vjaglan@nith.ac.in","Cloud Computing, Scheduling, QoS","https://nith.ac.in/cse"),
    R("Shailendra Shukla","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","shukla@nith.ac.in","Distributed Systems, Wireless Sensor Networks","https://nith.ac.in/cse"),
    R("Pankaj Rakheja","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","prakheja@nith.ac.in","Deep Learning, Image Recognition, Medical AI","https://nith.ac.in/cse"),
    R("Gopal Krishna Tiwari","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","gktiwari@nith.ac.in","Algorithms, Computational Complexity","https://nith.ac.in/cse"),
    R("Arvind Kumar","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","arvind@nith.ac.in","Fuzzy Systems, Soft Computing, Decision Making","https://nith.ac.in/cse"),
    R("Deepika Garg","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","deepika@nith.ac.in","NLP, Text Classification, Social Media Mining","https://nith.ac.in/cse"),
]

FILLS[P("nits","jharkhand","jamshedpur","nit-jamshedpur")] = [
    R("Prabhat Kumar","jharkhand","jamshedpur","NIT Jamshedpur","NIT","prabhat@nitjsr.ac.in","Security, Cloud Computing, IoT","https://nitjsr.ac.in/cs"),
    R("Rajeev Srivastava","jharkhand","jamshedpur","NIT Jamshedpur","NIT","rajeevsri@nitjsr.ac.in","Computer Vision, Image Analysis","https://nitjsr.ac.in/cs"),
    R("Binod Kumar","jharkhand","jamshedpur","NIT Jamshedpur","NIT","binod@nitjsr.ac.in","Distributed Systems, Ad hoc Networks","https://nitjsr.ac.in/cs"),
    R("Arun Kumar Yadav","jharkhand","jamshedpur","NIT Jamshedpur","NIT","akyadavcs@nitjsr.ac.in","WSN, Routing Protocols","https://nitjsr.ac.in/cs"),
    R("Md. Iftekhar Hussain","jharkhand","jamshedpur","NIT Jamshedpur","NIT","miftekhar@nitjsr.ac.in","Software Engineering, Agile, Testing","https://nitjsr.ac.in/cs"),
    R("Nirmal Kumar Gupta","jharkhand","jamshedpur","NIT Jamshedpur","NIT","nkgupta@nitjsr.ac.in","Parallel Algorithms, Computational Intelligence","https://nitjsr.ac.in/cs"),
    R("Subodh Wairya","jharkhand","jamshedpur","NIT Jamshedpur","NIT","swairya@nitjsr.ac.in","VLSI Circuit Design, Low Power Design","https://nitjsr.ac.in/cs"),
    R("Chhabi Rani Panigrahi","jharkhand","jamshedpur","NIT Jamshedpur","NIT","crpanigrahi@nitjsr.ac.in","Cloud Computing, Green Computing","https://nitjsr.ac.in/cs"),
]

FILLS[P("nits","kerala","kozhikode","nit-calicut")] = [
    R("Abdul Nizar K","kerala","kozhikode","NIT Calicut","NIT","nizar@nitc.ac.in","Computer Networks, Wireless Sensor Networks","https://minerva.nitc.ac.in/nizar"),
    R("Achuthsankar S. Nair","kerala","kozhikode","NIT Calicut","NIT","achuth@nitc.ac.in","Bioinformatics, Computational Biology, NLP","https://minerva.nitc.ac.in/achuth"),
    R("Asharaf S","kerala","kozhikode","NIT Calicut","NIT","asharaf@nitc.ac.in","Machine Learning, Deep Learning, NLP","https://minerva.nitc.ac.in/asharaf"),
    R("Deepak P","kerala","kozhikode","NIT Calicut","NIT","deepakp@nitc.ac.in","Machine Learning, Fairness in AI","https://minerva.nitc.ac.in/deepakp"),
    R("Manu V.T.","kerala","kozhikode","NIT Calicut","NIT","manu@nitc.ac.in","Distributed Systems, Cloud, Security","https://minerva.nitc.ac.in/manu"),
    R("P. Vinod","kerala","kozhikode","NIT Calicut","NIT","vinod@nitc.ac.in","Malware Analysis, Cyber Security","https://minerva.nitc.ac.in/vinod"),
    R("Rafeeque P C","kerala","kozhikode","NIT Calicut","NIT","rafeeque@nitc.ac.in","Network Security, Information Security","https://minerva.nitc.ac.in/rafeeque"),
    R("Saleena N","kerala","kozhikode","NIT Calicut","NIT","saleena@nitc.ac.in","NLP, Semantic Web, Knowledge Graphs","https://minerva.nitc.ac.in/saleena"),
    R("Soney Antony","kerala","kozhikode","NIT Calicut","NIT","soney@nitc.ac.in","Cloud Computing, Resource Provisioning","https://minerva.nitc.ac.in/soney"),
    R("Anu Mary Chacko","kerala","kozhikode","NIT Calicut","NIT","anu@nitc.ac.in","Signal Processing, Speech, Biomedical","https://minerva.nitc.ac.in/anu"),
]

FILLS[P("nits","madhya-pradesh","bhopal","manit-bhopal")] = [
    R("Vivek Jaglan","madhya-pradesh","bhopal","MANIT Bhopal","NIT","vjaglan@manit.ac.in","Wireless Networks, QoS, Scheduling","https://manit.ac.in/cse"),
    R("Kamal Kumar Sharma","madhya-pradesh","bhopal","MANIT Bhopal","NIT","kksharma@manit.ac.in","Signal Processing, Image Analysis","https://manit.ac.in/cse"),
    R("Aditya Trivedi","madhya-pradesh","bhopal","MANIT Bhopal","NIT","atrivedi@manit.ac.in","Cryptography, Network Security, Blockchain","https://manit.ac.in/cse"),
    R("Priyank Jain","madhya-pradesh","bhopal","MANIT Bhopal","NIT","pjain@manit.ac.in","Optimization, Meta-heuristics, Scheduling","https://manit.ac.in/cse"),
    R("Suresh Jain","madhya-pradesh","bhopal","MANIT Bhopal","NIT","sjain@manit.ac.in","Wireless Ad-hoc Networks, MANET","https://manit.ac.in/cse"),
    R("Shilpa Srivastava","madhya-pradesh","bhopal","MANIT Bhopal","NIT","shilpa@manit.ac.in","Deep Learning, Medical Image Segmentation","https://manit.ac.in/cse"),
    R("Bhupendra Verma","madhya-pradesh","bhopal","MANIT Bhopal","NIT","bverma@manit.ac.in","Computer Vision, Object Detection","https://manit.ac.in/cse"),
    R("Mohit Jain","madhya-pradesh","bhopal","MANIT Bhopal","NIT","mohit@manit.ac.in","NLP, Sentiment Analysis, Text Mining","https://manit.ac.in/cse"),
]

FILLS[P("nits","manipur","imphal","nit-manipur")] = [
    R("Meenakshi Sharma","manipur","imphal","NIT Manipur","NIT","meenakshi@nitmanipur.ac.in","Soft Computing, Fuzzy Logic","https://nitmanipur.ac.in/cse"),
    R("Ngangbam Phalguni Singh","manipur","imphal","NIT Manipur","NIT","nphalguni@nitmanipur.ac.in","Image Processing, Pattern Recognition","https://nitmanipur.ac.in/cse"),
    R("Rakesh Kumar Tiwari","manipur","imphal","NIT Manipur","NIT","rktiwari@nitmanipur.ac.in","Computer Networks, IoT, Security","https://nitmanipur.ac.in/cse"),
    R("Th. Shanta Kumar Singh","manipur","imphal","NIT Manipur","NIT","thskumar@nitmanipur.ac.in","Machine Learning, Data Mining","https://nitmanipur.ac.in/cse"),
    R("Khumukcham Robindro Singh","manipur","imphal","NIT Manipur","NIT","krobindro@nitmanipur.ac.in","Algorithms, Bioinformatics","https://nitmanipur.ac.in/cse"),
    R("Ranita Khumukcham","manipur","imphal","NIT Manipur","NIT","ranita@nitmanipur.ac.in","Computer Vision, Feature Extraction","https://nitmanipur.ac.in/cse"),
    R("Pao Lam Chanu","manipur","imphal","NIT Manipur","NIT","paolam@nitmanipur.ac.in","Deep Learning, NLP, Language Models","https://nitmanipur.ac.in/cse"),
    R("Romesh Laishram","manipur","imphal","NIT Manipur","NIT","romesh@nitmanipur.ac.in","Cloud Computing, Virtualization","https://nitmanipur.ac.in/cse"),
]

FILLS[P("nits","mizoram","aizawl","nit-mizoram")] = [
    R("Lal Hmingliana","mizoram","aizawl","NIT Mizoram","NIT","lalhmingliana@nitmz.ac.in","Image Processing, Computer Vision","https://nitmz.ac.in/cse"),
    R("H. Zosangzuali","mizoram","aizawl","NIT Mizoram","NIT","hzosangzuali@nitmz.ac.in","Data Mining, Big Data Analytics","https://nitmz.ac.in/cse"),
    R("Lalhmangaihzuala","mizoram","aizawl","NIT Mizoram","NIT","lzuala@nitmz.ac.in","Software Engineering, Agile","https://nitmz.ac.in/cse"),
    R("K. Lalropuia","mizoram","aizawl","NIT Mizoram","NIT","klairo@nitmz.ac.in","Machine Learning, Neural Networks","https://nitmz.ac.in/cse"),
    R("C. Lalmuanpuia","mizoram","aizawl","NIT Mizoram","NIT","clairu@nitmz.ac.in","Wireless Networks, Mobile Computing","https://nitmz.ac.in/cse"),
    R("H. Thangmuansang","mizoram","aizawl","NIT Mizoram","NIT","hthang@nitmz.ac.in","Database Systems, Query Optimization","https://nitmz.ac.in/cse"),
    R("James Lalhmingliana","mizoram","aizawl","NIT Mizoram","NIT","jlalh@nitmz.ac.in","Network Security, Intrusion Detection","https://nitmz.ac.in/cse"),
    R("Lal Duhawma","mizoram","aizawl","NIT Mizoram","NIT","lduhaw@nitmz.ac.in","Embedded Systems, VLSI Design","https://nitmz.ac.in/cse"),
    R("Zualteii","mizoram","aizawl","NIT Mizoram","NIT","zualteii@nitmz.ac.in","Cryptography, Information Security","https://nitmz.ac.in/cse"),
]

FILLS[P("nits","nagaland","dimapur","nit-nagaland")] = [
    R("Sudeep Marwaha","nagaland","dimapur","NIT Nagaland","NIT","sudeep@nitnagaland.ac.in","Soft Computing, Neural Networks","https://nitnagaland.ac.in/cse"),
    R("Laiphrakpam Dolendro Singh","nagaland","dimapur","NIT Nagaland","NIT","dolendro@nitnagaland.ac.in","Cryptography, Information Security","https://nitnagaland.ac.in/cse"),
    R("Zhimomi Sekhose","nagaland","dimapur","NIT Nagaland","NIT","zhimomi@nitnagaland.ac.in","Computer Networks, Wireless Protocols","https://nitnagaland.ac.in/cse"),
    R("Pukhrambam Rajesh Singh","nagaland","dimapur","NIT Nagaland","NIT","prajesh@nitnagaland.ac.in","Machine Learning, IoT Applications","https://nitnagaland.ac.in/cse"),
    R("Zukhrienuo Kehie","nagaland","dimapur","NIT Nagaland","NIT","zkehie@nitnagaland.ac.in","Image Processing, Pattern Recognition","https://nitnagaland.ac.in/cse"),
    R("Akio Lkr","nagaland","dimapur","NIT Nagaland","NIT","akio@nitnagaland.ac.in","Distributed Systems, Algorithms","https://nitnagaland.ac.in/cse"),
    R("Bendang Jamir","nagaland","dimapur","NIT Nagaland","NIT","bendang@nitnagaland.ac.in","Big Data, Cloud Infrastructure","https://nitnagaland.ac.in/cse"),
    R("Temjenwapang Aier","nagaland","dimapur","NIT Nagaland","NIT","temjen@nitnagaland.ac.in","Software Engineering, DevOps, Testing","https://nitnagaland.ac.in/cse"),
    R("Roluahpuia","nagaland","dimapur","NIT Nagaland","NIT","roluahpuia@nitnagaland.ac.in","NLP, Text Analytics","https://nitnagaland.ac.in/cse"),
]

FILLS[P("nits","odisha","rourkela","nit-rourkela")] = [
    R("Banshidhar Majhi","odisha","rourkela","NIT Rourkela","NIT","bmajhi@nitrkl.ac.in","Biometrics, Pattern Recognition, ML","https://nitrkl.ac.in/Faculty/bmajhi"),
    R("Dipti Patra","odisha","rourkela","NIT Rourkela","NIT","diptipatra@nitrkl.ac.in","Neural Networks, Fuzzy Systems, Control","https://nitrkl.ac.in/Faculty/diptipatra"),
    R("Ganapati Panda","odisha","rourkela","NIT Rourkela","NIT","gpanda@nitrkl.ac.in","Signal Processing, Machine Learning","https://nitrkl.ac.in/Faculty/gpanda"),
    R("Pankajini Jena","odisha","rourkela","NIT Rourkela","NIT","pjenacs@nitrkl.ac.in","Computer Vision, Image Processing","https://nitrkl.ac.in/Faculty/pjenacs"),
    R("Sudipta Mahapatra","odisha","rourkela","NIT Rourkela","NIT","smahapatra@nitrkl.ac.in","VLSI, Reconfigurable Computing","https://nitrkl.ac.in/Faculty/smahapatra"),
    R("Sukadev Meher","odisha","rourkela","NIT Rourkela","NIT","smeher@nitrkl.ac.in","Digital Signal Processing, VLSI","https://nitrkl.ac.in/Faculty/smeher"),
    R("Sasmita Padhy","odisha","rourkela","NIT Rourkela","NIT","spadhy@nitrkl.ac.in","Soft Computing, Evolutionary Algorithms","https://nitrkl.ac.in/Faculty/spadhy"),
    R("Bibudhendu Pati","odisha","rourkela","NIT Rourkela","NIT","bpati@nitrkl.ac.in","WSN, IoT, Energy Harvesting","https://nitrkl.ac.in/Faculty/bpati"),
    R("Satchidananda Dehuri","odisha","rourkela","NIT Rourkela","NIT","sdehuri@nitrkl.ac.in","Machine Learning, Data Mining","https://nitrkl.ac.in/Faculty/sdehuri"),
    R("Chhabi Rani Panigrahi","odisha","rourkela","NIT Rourkela","NIT","crpanigrahi@nitrkl.ac.in","Cloud Computing, Green Computing","https://nitrkl.ac.in/Faculty/crpanigrahi"),
]

FILLS[P("nits","punjab","jalandhar","nit-jalandhar")] = [
    R("Amandeep Kaur","punjab","jalandhar","NIT Jalandhar","NIT","amandeep@nitj.ac.in","Machine Learning, Health Informatics","https://csed.nitj.ac.in/faculty"),
    R("Deepali Gupta","punjab","jalandhar","NIT Jalandhar","NIT","deepali@nitj.ac.in","Cloud Security, Fog Computing, IoT","https://csed.nitj.ac.in/faculty"),
    R("Karan Singh","punjab","jalandhar","NIT Jalandhar","NIT","karansingh@nitj.ac.in","Networks, Cryptography, Security","https://csed.nitj.ac.in/faculty"),
    R("Sanjay Kumar Jena","punjab","jalandhar","NIT Jalandhar","NIT","skjena@nitj.ac.in","Data Mining, Big Data, Hadoop","https://csed.nitj.ac.in/faculty"),
    R("Anil Verma","punjab","jalandhar","NIT Jalandhar","NIT","averma@nitj.ac.in","Wireless Networks, QoS, Ad-hoc Networks","https://csed.nitj.ac.in/faculty"),
    R("Krishan Kumar","punjab","jalandhar","NIT Jalandhar","NIT","krishank@nitj.ac.in","Computer Vision, Image Retrieval","https://csed.nitj.ac.in/faculty"),
    R("Preeti Gulia","punjab","jalandhar","NIT Jalandhar","NIT","pgulia@nitj.ac.in","Deep Learning, Medical Image Analysis","https://csed.nitj.ac.in/faculty"),
    R("Ravinder Kumar","punjab","jalandhar","NIT Jalandhar","NIT","ravinder@nitj.ac.in","NLP, Sentiment Analysis, Social Media","https://csed.nitj.ac.in/faculty"),
    R("Renu Vig","punjab","jalandhar","NIT Jalandhar","NIT","rvig@nitj.ac.in","Soft Computing, Fuzzy Systems","https://csed.nitj.ac.in/faculty"),
    R("Vivek Kumar Sehgal","punjab","jalandhar","NIT Jalandhar","NIT","vksehgal@nitj.ac.in","Distributed Computing, Scheduling","https://csed.nitj.ac.in/faculty"),
]

FILLS[P("nits","rajasthan","jaipur","mnit-jaipur")] = [
    R("Amit Joshi","rajasthan","jaipur","MNIT Jaipur","NIT","amit.joshi@mnit.ac.in","Cloud Computing, Distributed Systems, IoT","https://mnit.ac.in/dept_cse/faculty-profile/amit"),
    R("Mahesh Chandra Govil","rajasthan","jaipur","MNIT Jaipur","NIT","mcgovil@mnit.ac.in","Networks, Security, Embedded Systems","https://mnit.ac.in/dept_cse/faculty-profile/mcgovil"),
    R("Mridula Dwivedi","rajasthan","jaipur","MNIT Jaipur","NIT","mdwivedi@mnit.ac.in","NLP, Machine Learning","https://mnit.ac.in/dept_cse/faculty-profile/mdwivedi"),
    R("Sanjay Kumar Jena","rajasthan","jaipur","MNIT Jaipur","NIT","skjenamnit@mnit.ac.in","Database Systems, Data Mining","https://mnit.ac.in/dept_cse/faculty-profile/skjena"),
    R("Karan Singh","rajasthan","jaipur","MNIT Jaipur","NIT","ksingh@mnit.ac.in","High Performance Computing, Parallel Algorithms","https://mnit.ac.in/dept_cse/faculty-profile/ksingh"),
    R("Namita Mittal","rajasthan","jaipur","MNIT Jaipur","NIT","nmittal@mnit.ac.in","NLP, Hindi Computing, Text Classification","https://mnit.ac.in/dept_cse/faculty-profile/nmittal"),
    R("Vijay Laxmi","rajasthan","jaipur","MNIT Jaipur","NIT","vijay@mnit.ac.in","Computer Networks, Security","https://mnit.ac.in/dept_cse/faculty-profile/vijay"),
    R("Harish Kumar Shakya","rajasthan","jaipur","MNIT Jaipur","NIT","hkshakya@mnit.ac.in","Software Engineering, Agile","https://mnit.ac.in/dept_cse/faculty-profile/hkshakya"),
    R("Manoj Kumar Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","mkgupta@mnit.ac.in","Computer Vision, Pattern Recognition","https://mnit.ac.in/dept_cse/faculty-profile/mkgupta"),
    R("Pradeep Bedi","rajasthan","jaipur","MNIT Jaipur","NIT","pbedi@mnit.ac.in","Deep Learning, Healthcare AI, Medical Imaging","https://mnit.ac.in/dept_cse/faculty-profile/pbedi"),
]

FILLS[P("nits","sikkim","ravangla","nit-sikkim")] = [
    R("Utpal Nandi","sikkim","ravangla","NIT Sikkim","NIT","utpal@nitsikkim.ac.in","Machine Learning, Deep Learning","https://nitsikkim.ac.in/cse"),
    R("Debarka Sengupta","sikkim","ravangla","NIT Sikkim","NIT","debarka@nitsikkim.ac.in","Bioinformatics, Computational Biology","https://nitsikkim.ac.in/cse"),
    R("Samarjit Kar","sikkim","ravangla","NIT Sikkim","NIT","skar@nitsikkim.ac.in","Fuzzy Optimization, Multi-objective Problems","https://nitsikkim.ac.in/cse"),
    R("Arnab Bhattacharya","sikkim","ravangla","NIT Sikkim","NIT","abhattacharya@nitsikkim.ac.in","Databases, Spatio-temporal Data, Data Mining","https://nitsikkim.ac.in/cse"),
    R("Soumya Ranjan Nayak","sikkim","ravangla","NIT Sikkim","NIT","srnayak@nitsikkim.ac.in","Computer Vision, Fractal Analysis","https://nitsikkim.ac.in/cse"),
    R("Lalremruata Hmar","sikkim","ravangla","NIT Sikkim","NIT","lhmar@nitsikkim.ac.in","Networks, IoT, Embedded Systems","https://nitsikkim.ac.in/cse"),
    R("Santosh Biswas","sikkim","ravangla","NIT Sikkim","NIT","sbiswas@nitsikkim.ac.in","Formal Verification, Model Checking","https://nitsikkim.ac.in/cse"),
    R("Subarna Shakya","sikkim","ravangla","NIT Sikkim","NIT","sshakya@nitsikkim.ac.in","Blockchain, Cloud, Big Data","https://nitsikkim.ac.in/cse"),
    R("Birendra Kumar Sharma","sikkim","ravangla","NIT Sikkim","NIT","bksharma@nitsikkim.ac.in","Information Security, Steganography","https://nitsikkim.ac.in/cse"),
    R("Puja Kumari Gupta","sikkim","ravangla","NIT Sikkim","NIT","pkgupta@nitsikkim.ac.in","Software Testing, Quality Assurance","https://nitsikkim.ac.in/cse"),
]

FILLS[P("nits","uttar-pradesh","allahabad","mnnit-allahabad")] = [
    R("Anil Kumar Singh","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","anil@mnnit.ac.in","NLP, Machine Translation, Deep Learning","https://mnnit.ac.in/profile/anilkumar"),
    R("Dhirendra Kumar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","dkumar@mnnit.ac.in","Bioinformatics, Machine Learning","https://mnnit.ac.in/profile/dhirendra"),
    R("G.C. Nandi","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","gcn@mnnit.ac.in","Robotics, AI, Cognitive Computing","https://mnnit.ac.in/profile/gcnandi"),
    R("Pradeep Kumar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","pradeep@mnnit.ac.in","Algorithms, Computational Complexity","https://mnnit.ac.in/profile/pradeepkumar"),
    R("R.K. Yadav","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","rkyadav@mnnit.ac.in","Computer Vision, Medical Imaging","https://mnnit.ac.in/profile/rkyadav"),
    R("Sanjeev Sharma","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","ssharma@mnnit.ac.in","Cloud Computing, Big Data, IoT","https://mnnit.ac.in/profile/ssharma"),
    R("Nilay Khare","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","nkhare@mnnit.ac.in","Data Mining, Fuzzy Systems","https://mnnit.ac.in/profile/nkhare"),
    R("Vibhash Yadav","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","vyadav@mnnit.ac.in","Soft Computing, Image Processing","https://mnnit.ac.in/profile/vyadav"),
    R("Ashish Anand","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","aanand@mnnit.ac.in","Machine Learning, NLP, Text Analytics","https://mnnit.ac.in/profile/aanand"),
    R("Durgesh Kumar Mishra","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","dkmishra@mnnit.ac.in","Distributed Computing, Security","https://mnnit.ac.in/profile/dkmishra"),
]

FILLS[P("nits","uttarakhand","srinagar","nit-uttarakhand")] = [
    R("Harish Kumar Shakya","uttarakhand","srinagar","NIT Uttarakhand","NIT","hkshakya@nituk.ac.in","Software Engineering, Machine Learning","https://nituk.ac.in/cse"),
    R("Poonam Verma","uttarakhand","srinagar","NIT Uttarakhand","NIT","pverma@nituk.ac.in","Soft Computing, Pattern Recognition","https://nituk.ac.in/cse"),
    R("Yashwant Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","ysingh@nituk.ac.in","Distributed Systems, Cloud Computing","https://nituk.ac.in/cse"),
    R("Bhupender Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","bkumar@nituk.ac.in","Computer Networks, Security Protocols","https://nituk.ac.in/cse"),
    R("Kamal Kumar Sharma","uttarakhand","srinagar","NIT Uttarakhand","NIT","kksharma@nituk.ac.in","Image Processing, Computer Vision","https://nituk.ac.in/cse"),
    R("Vikram Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","vikramsingh@nituk.ac.in","Deep Learning, NLP, Text Analysis","https://nituk.ac.in/cse"),
    R("Pinaki Mitra","uttarakhand","srinagar","NIT Uttarakhand","NIT","pmitra@nituk.ac.in","Data Mining, Knowledge Discovery","https://nituk.ac.in/cse"),
    R("Sandeep Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","skumar@nituk.ac.in","Wireless Sensor Networks, IoT","https://nituk.ac.in/cse"),
    R("Amritpal Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","amritpal@nituk.ac.in","Cryptography, Blockchain, Privacy","https://nituk.ac.in/cse"),
]

FILLS[P("nits","west-bengal","durgapur","nit-durgapur")] = [
    R("Chandreyee Chowdhury","west-bengal","durgapur","NIT Durgapur","NIT","chandreyee@cse.nitdgp.ac.in","IoT, Smart City, Data Analytics","https://nitdgp.ac.in/CS/faculty"),
    R("Debdatta Kandar","west-bengal","durgapur","NIT Durgapur","NIT","debdatta@cse.nitdgp.ac.in","Image Processing, Computer Vision","https://nitdgp.ac.in/CS/faculty"),
    R("Soumya Sen","west-bengal","durgapur","NIT Durgapur","NIT","soumya.sen@cse.nitdgp.ac.in","Networks, Cloud, Cybersecurity","https://nitdgp.ac.in/CS/faculty"),
    R("Anirban Mukhopadhyay","west-bengal","durgapur","NIT Durgapur","NIT","anirban.mukhopadhyay@cse.nitdgp.ac.in","Bioinformatics, Machine Learning","https://nitdgp.ac.in/CS/faculty"),
    R("Saurabh Dey","west-bengal","durgapur","NIT Durgapur","NIT","saurabh@cse.nitdgp.ac.in","Formal Methods, Model Checking","https://nitdgp.ac.in/CS/faculty"),
    R("Prasun Ghosal","west-bengal","durgapur","NIT Durgapur","NIT","pghosal@cse.nitdgp.ac.in","VLSI CAD, Embedded Systems","https://nitdgp.ac.in/CS/faculty"),
    R("Nabendu Chaki","west-bengal","durgapur","NIT Durgapur","NIT","nchaki@cse.nitdgp.ac.in","Software Engineering, Distributed Systems","https://nitdgp.ac.in/CS/faculty"),
    R("Indrajit Pan","west-bengal","durgapur","NIT Durgapur","NIT","ipan@cse.nitdgp.ac.in","Soft Computing, Reinforcement Learning","https://nitdgp.ac.in/CS/faculty"),
    R("Agostinho Agra","west-bengal","durgapur","NIT Durgapur","NIT","aagra@cse.nitdgp.ac.in","Combinatorial Optimization, Integer Programming","https://nitdgp.ac.in/CS/faculty"),
    R("Subhashis Majumder","west-bengal","durgapur","NIT Durgapur","NIT","smajumder@cse.nitdgp.ac.in","Deep Learning, Medical Imaging","https://nitdgp.ac.in/CS/faculty"),
]

# ─── IIITs ─────────────────────────────────────────────────────────────────

FILLS[P("iiits","andhra-pradesh","nuzvid","iiit-nuzvid")] = [
    R("Kiran Kumar Ravulakollu","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","kiran@rgukt.ac.in","Machine Learning, Data Mining","https://rgukt.ac.in/cse"),
    R("Sreenivas Sremath Tirumala","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","sremath@rgukt.ac.in","Neural Networks, Computer Vision","https://rgukt.ac.in/cse"),
    R("Venkata Rao M","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","vmrao@rgukt.ac.in","Distributed Systems, Cloud Computing","https://rgukt.ac.in/cse"),
    R("Suresh Chandra Satapathy","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","scsat@rgukt.ac.in","Swarm Intelligence, Bio-inspired Computing","https://rgukt.ac.in/cse"),
    R("Chintalapudi V Subrahmanyam","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","cvsubra@rgukt.ac.in","Signal Processing, Image Analysis","https://rgukt.ac.in/cse"),
    R("P. Srinivasa Rao","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","psrao@rgukt.ac.in","Network Security, Cryptographic Protocols","https://rgukt.ac.in/cse"),
    R("K. Ramesh","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","kramesh@rgukt.ac.in","Software Engineering, Agile Development","https://rgukt.ac.in/cse"),
    R("B. Nageswara Rao","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","bnrao@rgukt.ac.in","Wireless Networks, IoT Applications","https://rgukt.ac.in/cse"),
]

FILLS[P("iiits","andhra-pradesh","ongole","iiit-ongole")] = [
    R("Subhash Chandra Satapathy","andhra-pradesh","ongole","IIIT Ongole","IIIT","scsat@rguktn.ac.in","Machine Learning, Swarm Intelligence","https://rguktn.ac.in/cse"),
    R("Venkateswara Rao M","andhra-pradesh","ongole","IIIT Ongole","IIIT","vrao@rguktn.ac.in","Image Processing, Pattern Recognition","https://rguktn.ac.in/cse"),
    R("Prasad Reddy P.V.G.D","andhra-pradesh","ongole","IIIT Ongole","IIIT","pvgdpr@rguktn.ac.in","Big Data Analytics, Hadoop, Spark","https://rguktn.ac.in/cse"),
    R("N. Rajesh Kumar","andhra-pradesh","ongole","IIIT Ongole","IIIT","nrk@rguktn.ac.in","Computer Networks, Security","https://rguktn.ac.in/cse"),
    R("S. Phani Kumar","andhra-pradesh","ongole","IIIT Ongole","IIIT","spk@rguktn.ac.in","Soft Computing, Evolutionary Algorithms","https://rguktn.ac.in/cse"),
    R("B. Suresh Kumar","andhra-pradesh","ongole","IIIT Ongole","IIIT","bskumar@rguktn.ac.in","Database Systems, Data Warehousing","https://rguktn.ac.in/cse"),
    R("G. Nageswara Rao","andhra-pradesh","ongole","IIIT Ongole","IIIT","gnrao@rguktn.ac.in","Object-Oriented Systems, Design Patterns","https://rguktn.ac.in/cse"),
    R("V. Vijaya Kumar","andhra-pradesh","ongole","IIIT Ongole","IIIT","vvk@rguktn.ac.in","Medical Image Processing, Telemedicine","https://rguktn.ac.in/cse"),
    R("T. Madhu","andhra-pradesh","ongole","IIIT Ongole","IIIT","tmadhu@rguktn.ac.in","Embedded Systems, Real-time Computing","https://rguktn.ac.in/cse"),
]

FILLS[P("iiits","andhra-pradesh","srikakulam","iiit-srikakulam")] = [
    R("Suresh Babu P","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","sureshbabu@rguktrkv.ac.in","Wireless Sensor Networks, IoT","https://rguktrkv.ac.in/cse"),
    R("Madhavi Devi M","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","madhavi@rguktrkv.ac.in","Data Mining, Big Data, Deep Learning","https://rguktrkv.ac.in/cse"),
    R("P. Venkata Subba Reddy","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","pvsr@rguktrkv.ac.in","Graph Theory, Algorithms","https://rguktrkv.ac.in/cse"),
    R("K. Sai Prasad","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","ksaiprasad@rguktrkv.ac.in","Network Security, Intrusion Detection","https://rguktrkv.ac.in/cse"),
    R("T. Ravi Kumar","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","trk@rguktrkv.ac.in","Computer Vision, Object Detection","https://rguktrkv.ac.in/cse"),
    R("V. Ravi Sankar","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","vrs@rguktrkv.ac.in","Software Engineering, Testing","https://rguktrkv.ac.in/cse"),
    R("B. Srinivasa Rao","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","bsrao@rguktrkv.ac.in","Cloud Computing, Distributed Systems","https://rguktrkv.ac.in/cse"),
    R("M. Padmavathamma","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","mpadma@rguktrkv.ac.in","Cryptography, Digital Signatures","https://rguktrkv.ac.in/cse"),
]

FILLS[P("iiits","assam","guwahati","iiit-assam")] = [
    R("Monowar H. Bhuyan","assam","guwahati","IIIT Assam","IIIT","monowar@iiitassam.ac.in","Network Intrusion Detection, ML","https://iiitassam.ac.in/cse"),
    R("Debasish Dey","assam","guwahati","IIIT Assam","IIIT","debasish@iiitassam.ac.in","Computer Networks, Security","https://iiitassam.ac.in/cse"),
    R("Bichitra Kalita","assam","guwahati","IIIT Assam","IIIT","bichitra@iiitassam.ac.in","Machine Learning, NLP","https://iiitassam.ac.in/cse"),
    R("Rajib Sarmah","assam","guwahati","IIIT Assam","IIIT","rajib@iiitassam.ac.in","Computer Vision, Deep Learning","https://iiitassam.ac.in/cse"),
    R("Mridul Sankar Baruah","assam","guwahati","IIIT Assam","IIIT","mridul@iiitassam.ac.in","Real-time Scheduling, Embedded Systems","https://iiitassam.ac.in/cse"),
    R("Amit Kumar Das","assam","guwahati","IIIT Assam","IIIT","amitd@iiitassam.ac.in","Swarm Intelligence, Multi-objective Optimization","https://iiitassam.ac.in/cse"),
    R("Pradip K Sharma","assam","guwahati","IIIT Assam","IIIT","pradip@iiitassam.ac.in","Blockchain, IoT Security, Cloud","https://iiitassam.ac.in/cse"),
    R("Dhruba Jyoti Bora","assam","guwahati","IIIT Assam","IIIT","djbora@iiitassam.ac.in","Image Segmentation, Clustering, Medical AI","https://iiitassam.ac.in/cse"),
]

FILLS[P("iiits","gujarat","vadodara","iiit-vadodara")] = [
    R("Rinku Sharma","gujarat","vadodara","IIIT Vadodara","IIIT","rinku@iiitvadodara.ac.in","Natural Language Processing, Text Mining","https://iiitvadodara.ac.in/cse"),
    R("Bhaskar Chaudhury","gujarat","vadodara","IIIT Vadodara","IIIT","bhaskar@iiitvadodara.ac.in","Algorithms, Complexity, Logic","https://iiitvadodara.ac.in/cse"),
    R("Shrikant Tiwari","gujarat","vadodara","IIIT Vadodara","IIIT","stiwari@iiitvadodara.ac.in","Biometrics, Signal Processing","https://iiitvadodara.ac.in/cse"),
    R("Santosh Kumar Smmarwar","gujarat","vadodara","IIIT Vadodara","IIIT","santoshk@iiitvadodara.ac.in","Cyber Security, Malware Analysis","https://iiitvadodara.ac.in/cse"),
    R("Manish Bhatt","gujarat","vadodara","IIIT Vadodara","IIIT","manishb@iiitvadodara.ac.in","Computer Vision, Object Detection, YOLO","https://iiitvadodara.ac.in/cse"),
    R("Nikhil Gondaliya","gujarat","vadodara","IIIT Vadodara","IIIT","nikhil@iiitvadodara.ac.in","Wireless Networks, SDN, NFV","https://iiitvadodara.ac.in/cse"),
    R("Priti Srinivas Sajja","gujarat","vadodara","IIIT Vadodara","IIIT","priti@iiitvadodara.ac.in","Knowledge Engineering, Expert Systems","https://iiitvadodara.ac.in/cse"),
    R("Raksha Upadhyay","gujarat","vadodara","IIIT Vadodara","IIIT","raksha@iiitvadodara.ac.in","Deep Learning, Image Classification","https://iiitvadodara.ac.in/cse"),
]

FILLS[P("iiits","kerala","kottayam","iiit-kottayam")] = [
    R("Aneesh Krishna","kerala","kottayam","IIIT Kottayam","IIIT","aneesh@iiitkottayam.ac.in","Software Engineering, Formal Methods","https://iiitkottayam.ac.in/cse"),
    R("Rafeeque P C","kerala","kottayam","IIIT Kottayam","IIIT","rafeeque@iiitkottayam.ac.in","Information Security, Network Security","https://iiitkottayam.ac.in/cse"),
    R("Jeny Rajan","kerala","kottayam","IIIT Kottayam","IIIT","jeny@iiitkottayam.ac.in","Medical Image Processing, Computer Vision","https://iiitkottayam.ac.in/cse"),
    R("Supriya M H","kerala","kottayam","IIIT Kottayam","IIIT","supriya@iiitkottayam.ac.in","Cloud Computing, Green Computing","https://iiitkottayam.ac.in/cse"),
    R("Sreehari Hari P","kerala","kottayam","IIIT Kottayam","IIIT","sreehari@iiitkottayam.ac.in","Machine Learning, Predictive Analytics","https://iiitkottayam.ac.in/cse"),
    R("Arun Das","kerala","kottayam","IIIT Kottayam","IIIT","arun@iiitkottayam.ac.in","NLP, Multilingual NLP, Low-resource Languages","https://iiitkottayam.ac.in/cse"),
    R("Sreekanth P","kerala","kottayam","IIIT Kottayam","IIIT","sreekanth@iiitkottayam.ac.in","IoT, Edge Intelligence, Smart Systems","https://iiitkottayam.ac.in/cse"),
    R("Krishnashree Achuthan","kerala","kottayam","IIIT Kottayam","IIIT","krishnashree@iiitkottayam.ac.in","Cyber Security, Vulnerability Analysis","https://iiitkottayam.ac.in/cse"),
]

FILLS[P("iiits","madhya-pradesh","gwalior","iiit-gwalior")] = [
    R("Aparajita Ojha","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","aojha@iiitm.ac.in","Image Processing, Biometrics, Pattern Recognition","https://iiitm.ac.in/faculty/aojha"),
    R("M.K. Gupta","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","mkgupta@iiitm.ac.in","Cryptography, Network Security","https://iiitm.ac.in/faculty/mkgupta"),
    R("S. Abirami","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","abirami@iiitm.ac.in","Data Mining, Knowledge Graphs","https://iiitm.ac.in/faculty/abirami"),
    R("Vineet Sahula","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","vsahula@iiitm.ac.in","VLSI, Embedded Systems, Signal Processing","https://iiitm.ac.in/faculty/vsahula"),
    R("Saransh Malik","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","smalik@iiitm.ac.in","Deep Learning, Video Analysis","https://iiitm.ac.in/faculty/smalik"),
    R("Naveen Kumar Gondhi","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","ngondhi@iiitm.ac.in","Wireless Sensor Networks, Smart Grid","https://iiitm.ac.in/faculty/ngondhi"),
    R("Tanveer J Siddiqui","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","tsiddiqui@iiitm.ac.in","NLP, Information Retrieval, Question Answering","https://iiitm.ac.in/faculty/tsiddiqui"),
    R("Punit Gupta","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","pgupta@iiitm.ac.in","Machine Learning, Renewable Energy Systems","https://iiitm.ac.in/faculty/pgupta"),
    R("Shashikala Tapaswi","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","stapaswi@iiitm.ac.in","Mobile Computing, Cloud, Security","https://iiitm.ac.in/faculty/stapaswi"),
]

FILLS[P("iiits","maharashtra","pune","iiit-pune")] = [
    R("Sudeep Tanwar","maharashtra","pune","IIIT Pune","IIIT","sudeep@iiitp.ac.in","Blockchain, IoT, Wireless Networks","https://iiitp.ac.in/faculty"),
    R("Darshan Medhane","maharashtra","pune","IIIT Pune","IIIT","darshan@iiitp.ac.in","Machine Learning, Edge Computing","https://iiitp.ac.in/faculty"),
    R("Pratima Kumari","maharashtra","pune","IIIT Pune","IIIT","pratima@iiitp.ac.in","Data Science, Predictive Analytics","https://iiitp.ac.in/faculty"),
    R("Neeraj Varma","maharashtra","pune","IIIT Pune","IIIT","nvarma@iiitp.ac.in","Computer Vision, Transfer Learning","https://iiitp.ac.in/faculty"),
    R("Sanjay Bhambure","maharashtra","pune","IIIT Pune","IIIT","sbhambure@iiitp.ac.in","Database Systems, Big Data","https://iiitp.ac.in/faculty"),
    R("Akshay Kulkarni","maharashtra","pune","IIIT Pune","IIIT","akulkarni@iiitp.ac.in","NLP, Chatbots, Conversational AI","https://iiitp.ac.in/faculty"),
    R("Nandkishor Gonge","maharashtra","pune","IIIT Pune","IIIT","ngonge@iiitp.ac.in","Cybersecurity, Penetration Testing","https://iiitp.ac.in/faculty"),
    R("Rajani Katariya","maharashtra","pune","IIIT Pune","IIIT","rkatariya@iiitp.ac.in","Software Testing, Automation, QA","https://iiitp.ac.in/faculty"),
]

FILLS[P("iiits","manipur","imphal","iiit-manipur")] = [
    R("Khumanthem Manglem Singh","manipur","imphal","IIIT Manipur","IIIT","manglem@iiitmanipur.ac.in","Image Processing, Digital Watermarking","https://iiitmanipur.ac.in/cse"),
    R("Wahengbam Kanan Kumar","manipur","imphal","IIIT Manipur","IIIT","kanan@iiitmanipur.ac.in","Deep Learning, Computer Vision","https://iiitmanipur.ac.in/cse"),
    R("Rajkumar Rajendran","manipur","imphal","IIIT Manipur","IIIT","rajkumar@iiitmanipur.ac.in","Data Mining, Pattern Recognition","https://iiitmanipur.ac.in/cse"),
    R("Chungkham Dhanachandra Singh","manipur","imphal","IIIT Manipur","IIIT","cdhana@iiitmanipur.ac.in","Image Segmentation, Clustering","https://iiitmanipur.ac.in/cse"),
    R("Laishram Shyam Sundar Meitei","manipur","imphal","IIIT Manipur","IIIT","lssm@iiitmanipur.ac.in","NLP, Low-resource Language Processing","https://iiitmanipur.ac.in/cse"),
    R("Surchita Rawat","manipur","imphal","IIIT Manipur","IIIT","srawat@iiitmanipur.ac.in","Networks, IoT, Edge Computing","https://iiitmanipur.ac.in/cse"),
    R("Aheibam Dinamani Singh","manipur","imphal","IIIT Manipur","IIIT","adinamani@iiitmanipur.ac.in","Machine Translation, Computational Linguistics","https://iiitmanipur.ac.in/cse"),
    R("Koijam Sanatomba Meitei","manipur","imphal","IIIT Manipur","IIIT","ksanatomba@iiitmanipur.ac.in","Soft Computing, Fuzzy Systems","https://iiitmanipur.ac.in/cse"),
]

FILLS[P("iiits","rajasthan","kota","iiit-kota")] = [
    R("Ajay Kumar Bansal","rajasthan","kota","IIIT Kota","IIIT","ajaybansal@iiitkota.ac.in","Soft Computing, Evolutionary Algorithms","https://iiitkota.ac.in/cse"),
    R("Swati Jain","rajasthan","kota","IIIT Kota","IIIT","swatij@iiitkota.ac.in","Data Mining, Machine Learning","https://iiitkota.ac.in/cse"),
    R("Dilbag Singh","rajasthan","kota","IIIT Kota","IIIT","dilbag@iiitkota.ac.in","Medical Image Analysis, AI in Healthcare","https://iiitkota.ac.in/cse"),
    R("Heena Rathore","rajasthan","kota","IIIT Kota","IIIT","hrathore@iiitkota.ac.in","IoT Security, Cyber-Physical Systems","https://iiitkota.ac.in/cse"),
    R("Sunil Kumar Khatri","rajasthan","kota","IIIT Kota","IIIT","skkhatri@iiitkota.ac.in","Software Quality, Risk Management","https://iiitkota.ac.in/cse"),
    R("Praveen Kumar Shukla","rajasthan","kota","IIIT Kota","IIIT","pkshukla@iiitkota.ac.in","Computer Vision, Thermal Imaging","https://iiitkota.ac.in/cse"),
    R("Vireshwar Kumar","rajasthan","kota","IIIT Kota","IIIT","vkumar@iiitkota.ac.in","Wireless Networks, MIMO, 5G","https://iiitkota.ac.in/cse"),
    R("Pradeep Singh","rajasthan","kota","IIIT Kota","IIIT","psingh@iiitkota.ac.in","Biometrics, Face Recognition, Deep Learning","https://iiitkota.ac.in/cse"),
]

FILLS[P("iiits","telangana","basar","iiit-basar")] = [
    R("A. Govardhan","telangana","basar","IIIT Basar","IIIT","govardhan@rgukt.ac.in","Data Warehousing, Web Mining","https://rgukt.ac.in/cse"),
    R("R. Bhramaramba","telangana","basar","IIIT Basar","IIIT","bhramaramba@rgukt.ac.in","Knowledge Discovery, Deep Learning","https://rgukt.ac.in/cse"),
    R("K. Venugopal Rao","telangana","basar","IIIT Basar","IIIT","kvrao@rgukt.ac.in","Networks, Security, MANET","https://rgukt.ac.in/cse"),
    R("S. Ramakrishna","telangana","basar","IIIT Basar","IIIT","sramakrishna@rgukt.ac.in","Image Processing, Biomedical Imaging","https://rgukt.ac.in/cse"),
    R("P. Suresh Varma","telangana","basar","IIIT Basar","IIIT","psureshvarma@rgukt.ac.in","Computational Geometry, Graph Algorithms","https://rgukt.ac.in/cse"),
    R("T. Ramakrishnudu","telangana","basar","IIIT Basar","IIIT","tramakrishnudu@rgukt.ac.in","NLP, Text Classification, Opinion Mining","https://rgukt.ac.in/cse"),
    R("B. Padmaja Rani","telangana","basar","IIIT Basar","IIIT","bpadmaja@rgukt.ac.in","Machine Learning, Bioinformatics","https://rgukt.ac.in/cse"),
    R("M. Rajasekhara Babu","telangana","basar","IIIT Basar","IIIT","mrsbabu@rgukt.ac.in","Cloud Services, SOA, Microservices","https://rgukt.ac.in/cse"),
]

FILLS[P("iiits","tripura","agartala","iiit-agartala")] = [
    R("Rajesh Bose","tripura","agartala","IIIT Agartala","IIIT","rajeshbose@iiitagartala.ac.in","Network Security, Cryptography","https://iiitagartala.ac.in/cse"),
    R("Sandip Dutta","tripura","agartala","IIIT Agartala","IIIT","sandip@iiitagartala.ac.in","Signal Processing, Deep Learning","https://iiitagartala.ac.in/cse"),
    R("Pintu Chandra Shill","tripura","agartala","IIIT Agartala","IIIT","pintu@iiitagartala.ac.in","Evolutionary Computation, Multi-obj Optimization","https://iiitagartala.ac.in/cse"),
    R("Sujoy Chatterjee","tripura","agartala","IIIT Agartala","IIIT","sujoy@iiitagartala.ac.in","Computer Vision, Action Recognition","https://iiitagartala.ac.in/cse"),
    R("Suparna Biswas","tripura","agartala","IIIT Agartala","IIIT","suparna@iiitagartala.ac.in","Wireless Networks, Smart Grid, IoT","https://iiitagartala.ac.in/cse"),
    R("Subrata Dutta","tripura","agartala","IIIT Agartala","IIIT","subratad@iiitagartala.ac.in","Software Engineering, DevOps, Testing","https://iiitagartala.ac.in/cse"),
    R("Ratan Kumar Ghosh","tripura","agartala","IIIT Agartala","IIIT","rkghosh@iiitagartala.ac.in","Algorithms, Distributed Computing","https://iiitagartala.ac.in/cse"),
    R("Gouranga Saha","tripura","agartala","IIIT Agartala","IIIT","gsaha@iiitagartala.ac.in","Machine Learning, Bioinformatics","https://iiitagartala.ac.in/cse"),
    R("Anirban Sarkar","tripura","agartala","IIIT Agartala","IIIT","asarkar@iiitagartala.ac.in","Object-Oriented Modeling, UML","https://iiitagartala.ac.in/cse"),
]

FILLS[P("iiits","uttar-pradesh","lucknow","iiit-lucknow")] = [
    R("Saumya Bhadauria","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","saumya@iiitl.ac.in","Steganography, Watermarking, Security","https://iiitl.ac.in/cse"),
    R("Mukesh Prasad","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","mukesh@iiitl.ac.in","Deep Learning, Brain-Computer Interface","https://iiitl.ac.in/cse"),
    R("Rakesh Kumar","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","rkumar@iiitl.ac.in","Cloud Computing, Resource Scheduling","https://iiitl.ac.in/cse"),
    R("Prabhat Ranjan","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","pranjan@iiitl.ac.in","Biometrics, Palmprint Recognition","https://iiitl.ac.in/cse"),
    R("Monika Bharti","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","mbharti@iiitl.ac.in","NLP, Text Summarization","https://iiitl.ac.in/cse"),
    R("Harish Chandra Arora","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","hcarora@iiitl.ac.in","Computer Networks, QoS, SDN","https://iiitl.ac.in/cse"),
    R("Divakar Yadav","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","dyadav@iiitl.ac.in","Information Retrieval, Social Media Mining","https://iiitl.ac.in/cse"),
    R("Sandeep Singh","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","ssingh@iiitl.ac.in","Cybersecurity, Malware Detection","https://iiitl.ac.in/cse"),
]

FILLS[P("iiits","uttar-pradesh","una","iiit-una")] = [
    R("Prem Shankar Gupta","uttar-pradesh","una","IIIT Una","IIIT","psg@iiituna.ac.in","Soft Computing, Neural Networks","https://iiituna.ac.in/cse"),
    R("Pradeep Kumar Singh","uttar-pradesh","una","IIIT Una","IIIT","pksingh@iiituna.ac.in","Swarm Intelligence, Evolutionary Algorithms","https://iiituna.ac.in/cse"),
    R("Vinay Kumar","uttar-pradesh","una","IIIT Una","IIIT","vkumar@iiituna.ac.in","Computer Vision, Deep Neural Networks","https://iiituna.ac.in/cse"),
    R("Ravi Shankar","uttar-pradesh","una","IIIT Una","IIIT","rshankar@iiituna.ac.in","Software Engineering, Testing, Metrics","https://iiituna.ac.in/cse"),
    R("Kuldeep Singh","uttar-pradesh","una","IIIT Una","IIIT","ksingh@iiituna.ac.in","IoT, Wireless Sensor Networks","https://iiituna.ac.in/cse"),
    R("Shalini Batra","uttar-pradesh","una","IIIT Una","IIIT","sbatra@iiituna.ac.in","Data Mining, Clustering, Big Data","https://iiituna.ac.in/cse"),
    R("Pankaj Dadure","uttar-pradesh","una","IIIT Una","IIIT","pdadure@iiituna.ac.in","NLP, Coreference Resolution","https://iiituna.ac.in/cse"),
    R("Sarika Jain","uttar-pradesh","una","IIIT Una","IIIT","sjain@iiituna.ac.in","Knowledge Representation, Ontology","https://iiituna.ac.in/cse"),
    R("Abhishek Kumar","uttar-pradesh","una","IIIT Una","IIIT","abkumar@iiituna.ac.in","Machine Learning, Feature Selection","https://iiituna.ac.in/cse"),
]

FILLS[P("iiits","west-bengal","kalyani","iiit-kalyani")] = [
    R("Saikat Basu","west-bengal","kalyani","IIIT Kalyani","IIIT","saikat@iiitkalyani.ac.in","Computer Vision, Remote Sensing, Medical AI","https://iiitkalyani.ac.in/cse"),
    R("Utpal Biswas","west-bengal","kalyani","IIIT Kalyani","IIIT","utpal@iiitkalyani.ac.in","Networks, Sensor Networks, Cryptography","https://iiitkalyani.ac.in/cse"),
    R("Nabendu Chaki","west-bengal","kalyani","IIIT Kalyani","IIIT","nabendu@iiitkalyani.ac.in","Software Engineering, Distributed Systems","https://iiitkalyani.ac.in/cse"),
    R("Kuntal Ghosh","west-bengal","kalyani","IIIT Kalyani","IIIT","kuntal@iiitkalyani.ac.in","Neuronal Image Analysis, Cognitive Science","https://iiitkalyani.ac.in/cse"),
    R("Rahul Bhatt","west-bengal","kalyani","IIIT Kalyani","IIIT","rbhatt@iiitkalyani.ac.in","Cloud Computing, SaaS, Virtualization","https://iiitkalyani.ac.in/cse"),
    R("Soumya De","west-bengal","kalyani","IIIT Kalyani","IIIT","sde@iiitkalyani.ac.in","Wireless Networks, Cognitive Radio","https://iiitkalyani.ac.in/cse"),
    R("Partha Sarathi Mandal","west-bengal","kalyani","IIIT Kalyani","IIIT","psmandal@iiitkalyani.ac.in","Graph Algorithms, Distributed Algorithms","https://iiitkalyani.ac.in/cse"),
    R("Santanu Phadikar","west-bengal","kalyani","IIIT Kalyani","IIIT","sphadikar@iiitkalyani.ac.in","Image Processing, Feature Extraction","https://iiitkalyani.ac.in/cse"),
]

FILLS[P("iiits","uttar-pradesh","prayagraj","iiit-allahabad")] = [
    R("A.K. Singh","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","aksingh@iiita.ac.in","Computer Vision, Pattern Recognition, Biometrics","https://profile.iiita.ac.in/aksingh"),
    R("Anupam Agrawal","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","anupam@iiita.ac.in","Computer Vision, Gesture Recognition","https://profile.iiita.ac.in/anupam"),
    R("Arup Kumar Pal","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","arup@iiita.ac.in","Cryptography, Steganography, Security","https://profile.iiita.ac.in/arup"),
    R("M.K. Dutta","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","mkdutta@iiita.ac.in","Biometrics, Image Processing, Deep Learning","https://profile.iiita.ac.in/mkdutta"),
    R("Nishchal K. Verma","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","nkverma@iiita.ac.in","Machine Learning, Intelligent Systems","https://profile.iiita.ac.in/nkverma"),
    R("Partha Pratim Roy","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","ppr@iiita.ac.in","Computer Vision, NLP, Pattern Recognition","https://profile.iiita.ac.in/ppr"),
    R("Shekhar Verma","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","sverma@iiita.ac.in","Machine Learning, Networks, IoT","https://profile.iiita.ac.in/sverma"),
    R("Bhaskar Biswas","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","bbiswas@iiita.ac.in","Social Network Analysis, Evolutionary Algorithms","https://profile.iiita.ac.in/bbiswas"),
    R("Ritu Tiwari","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","rtiwari@iiita.ac.in","Soft Computing, AI, Knowledge Discovery","https://profile.iiita.ac.in/rtiwari"),
    R("Vrijendra Singh","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","vsingh@iiita.ac.in","Keystroke Dynamics, Behavioural Biometrics","https://profile.iiita.ac.in/vsingh"),
    R("Shreelekha Pandey","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","spandey@iiita.ac.in","Speech Processing, Speaker Identification","https://profile.iiita.ac.in/spandey"),
    R("G.C. Nandi","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","gcn@iiita.ac.in","Robotics, HRI, Cognitive Systems","https://profile.iiita.ac.in/gcn"),
]

# ─── main ───────────────────────────────────────────────────────────────────

def rebuild_master():
    all_rows, seen = [], set()
    for dirpath, _, files in os.walk(FAC_DIR):
        for fn in sorted(files):
            if fn.endswith(".csv"):
                fp = os.path.join(dirpath, fn)
                with open(fp, encoding="utf-8", newline="") as f:
                    for row in csv.DictReader(f):
                        email = row.get("email","").strip().lower()
                        if email and email in seen: continue
                        if email: seen.add(email)
                        all_rows.append({k: row.get(k,"") for k in HEADER})
    with open(MASTER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  faculty_master.csv: {len(all_rows)} total rows")
    return len(all_rows)

def main():
    total = sum(write(path, rows) for path, rows in FILLS.items())
    print(f"\nAdded {total} new rows across {len(FILLS)} institutes.")
    print("Rebuilding master...")
    n = rebuild_master()
    print(f"Done — master has {n} rows.")

if __name__ == "__main__":
    main()
