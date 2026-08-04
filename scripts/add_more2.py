#!/usr/bin/env python3
"""add_more2.py — push every CSV to 25+ rows, rebuild master."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FAC  = os.path.join(ROOT, "research", "faculty")
MASTER = os.path.join(ROOT, "research", "faculty_master.csv")
HEADER = ["name","state","city","institute","institute_type","department",
          "email","research_area","personal_site","priority","status","notes"]

def R(name,state,city,inst,it,email,area,site="",pri="1",st="queued",notes=""):
    return dict(name=name,state=state,city=city,institute=inst,
                institute_type=it,department="CSE",email=email,
                research_area=area,personal_site=site,
                priority=pri,status=st,notes=notes)

def existing(path):
    if not os.path.exists(path): return set()
    with open(path,encoding="utf-8") as f:
        return {r["email"].lower().strip() for r in csv.DictReader(f) if r.get("email")}

def write(path, rows):
    ex = existing(path)
    new = [r for r in rows if r["email"].lower() not in ex]
    if not new: return 0
    with open(path,"a",encoding="utf-8",newline="") as f:
        csv.DictWriter(f,fieldnames=HEADER).writerows(new)
    print(f"  +{len(new):2d}  {os.path.relpath(path,ROOT)}")
    return len(new)

def P(*p): return os.path.join(FAC,*p)+".csv"

FILLS = {}

# ── IIITs under 20 ──────────────────────────────────────────────────────────

FILLS[P("iiits","madhya-pradesh","gwalior","iiit-gwalior")] = [
    R("Abhishek Srivastava","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","asrivastava@iiitm.ac.in","Machine Learning, Neural Networks","https://iiitm.ac.in/faculty/asrivastava"),
    R("Anupam Dixit","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","adixit@iiitm.ac.in","Distributed Systems, Cloud Computing","https://iiitm.ac.in/faculty/adixit"),
    R("Arpan Pal","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","apal@iiitm.ac.in","IoT, Edge Computing, Pervasive Systems","https://iiitm.ac.in/faculty/apal"),
    R("Durgesh Kumar Mishra","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","dkmishra@iiitm.ac.in","Cloud Security, Distributed Systems","https://iiitm.ac.in/faculty/dkmishra"),
    R("Manish Shrivastava","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","mshrivastava@iiitm.ac.in","NLP, Language Resources, Morphology","https://iiitm.ac.in/faculty/mshrivastava"),
    R("Neetesh Kumar","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","nkumar@iiitm.ac.in","Soft Computing, Optimization, WSN","https://iiitm.ac.in/faculty/nkumar"),
    R("Poonam Yadav","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","pyadav@iiitm.ac.in","Image Processing, Medical Imaging","https://iiitm.ac.in/faculty/pyadav"),
    R("Praveen Kumar Shukla","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","pkshukla@iiitm.ac.in","Computer Vision, Thermal Imaging","https://iiitm.ac.in/faculty/pkshukla"),
    R("Rahul Katarya","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","rkatarya@iiitm.ac.in","Recommender Systems, Social Networks","https://iiitm.ac.in/faculty/rkatarya"),
    R("Richa Mishra","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","rmishra@iiitm.ac.in","Cryptography, Network Security","https://iiitm.ac.in/faculty/rmishra"),
    R("Sachin Tripathi","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","stripathi@iiitm.ac.in","Algorithms, Game Theory, Multi-agent","https://iiitm.ac.in/faculty/stripathi"),
    R("Sandeep Sharma","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","ssharma@iiitm.ac.in","Big Data, Hadoop, MapReduce","https://iiitm.ac.in/faculty/ssharma"),
    R("Smita Kasar","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","skasar@iiitm.ac.in","Deep Learning, Pattern Recognition","https://iiitm.ac.in/faculty/skasar"),
    R("Suresh Kumar Patel","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","skpatel@iiitm.ac.in","Computer Architecture, FPGA, Embedded","https://iiitm.ac.in/faculty/skpatel"),
]

FILLS[P("iiits","andhra-pradesh","srikakulam","iiit-srikakulam")] = [
    R("A. Ramamurthy","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","aramu2@rguktrkv.ac.in","Deep Learning, Autonomous Systems","https://rguktrkv.ac.in/cse"),
    R("B. Ramana Murthy","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","brmurthy@rguktrkv.ac.in","Computer Networks, Protocol Design","https://rguktrkv.ac.in/cse"),
    R("Ch. Venkata Ramana","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","cvramana@rguktrkv.ac.in","Data Mining, Warehousing","https://rguktrkv.ac.in/cse"),
    R("G. Hari Babu","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","ghbabu@rguktrkv.ac.in","Machine Learning, Neural Networks","https://rguktrkv.ac.in/cse"),
    R("K. Durga Prasad","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","kdprasad@rguktrkv.ac.in","Information Security, Blockchain","https://rguktrkv.ac.in/cse"),
    R("M. Rajkumar","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","mrajkumar@rguktrkv.ac.in","Image Processing, Biomedical","https://rguktrkv.ac.in/cse"),
    R("N. Balaji","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","nbalaji@rguktrkv.ac.in","Soft Computing, Evolutionary","https://rguktrkv.ac.in/cse"),
    R("P. Nagesh Babu","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","pnbabu@rguktrkv.ac.in","IoT, Edge Computing","https://rguktrkv.ac.in/cse"),
    R("R. Venkateswara Rao","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","rvrao@rguktrkv.ac.in","NLP, Sentiment Analysis","https://rguktrkv.ac.in/cse"),
    R("S. Lakshmana Rao","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","slrao@rguktrkv.ac.in","Embedded Systems, VLSI","https://rguktrkv.ac.in/cse"),
    R("T. Gopi Krishna","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","tgkrishna@rguktrkv.ac.in","Computer Vision, Object Detection","https://rguktrkv.ac.in/cse"),
    R("V. Lalitha","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","vlalitha@rguktrkv.ac.in","Cloud Computing, Virtualization","https://rguktrkv.ac.in/cse"),
    R("Y. V. S. Srinivasa Murthy","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","yvssmurthy@rguktrkv.ac.in","Algorithms, Graph Theory","https://rguktrkv.ac.in/cse"),
]

FILLS[P("iiits","telangana","hyderabad","iiit-hyderabad")] = [
    R("Anil Kumar Vuppala","telangana","hyderabad","IIIT Hyderabad","IIIT","anil.vuppala@iiit.ac.in","Speech Processing, Emotion Recognition","https://faculty.iiit.ac.in/~anil.vuppala"),
    R("Arjun Jain","telangana","hyderabad","IIIT Hyderabad","IIIT","arjun.jain@iiit.ac.in","Computer Vision, 3D Reconstruction","https://faculty.iiit.ac.in/~arjun.jain"),
    R("Bapi Raju Surampudi","telangana","hyderabad","IIIT Hyderabad","IIIT","bapi@iiit.ac.in","Computational Neuroscience, Brain Imaging","https://faculty.iiit.ac.in/~bapi"),
    R("Charu Sharma","telangana","hyderabad","IIIT Hyderabad","IIIT","charu.sharma@iiit.ac.in","NLP, Code-switching, Multilingual AI","https://faculty.iiit.ac.in/~charu.sharma"),
    R("Dipti Misra Sharma","telangana","hyderabad","IIIT Hyderabad","IIIT","dipti@iiit.ac.in","Computational Linguistics, NLP, Treebanks","https://faculty.iiit.ac.in/~dipti"),
    R("Kavita Vemuri","telangana","hyderabad","IIIT Hyderabad","IIIT","kavita.vemuri@iiit.ac.in","HCI, Cognitive Science, Affective Computing","https://faculty.iiit.ac.in/~kavita.vemuri"),
    R("Kishore Kothapalli","telangana","hyderabad","IIIT Hyderabad","IIIT","kkishore@iiit.ac.in","Parallel Algorithms, GPU, Distributed","https://faculty.iiit.ac.in/~kkishore"),
    R("Kushagra Tomer","telangana","hyderabad","IIIT Hyderabad","IIIT","kushagra@iiit.ac.in","Computer Vision, GANs, Image Synthesis","https://faculty.iiit.ac.in/~kushagra"),
    R("Laleh Jalali","telangana","hyderabad","IIIT Hyderabad","IIIT","laleh@iiit.ac.in","Software Engineering, Mining Software","https://faculty.iiit.ac.in/~laleh"),
    R("Ravi Kiran Sarvadevabhatla","telangana","hyderabad","IIIT Hyderabad","IIIT","ravi.kiran@iiit.ac.in","Computer Vision, Sketches, Creativity","https://faculty.iiit.ac.in/~ravi.kiran"),
    R("Shyam Sundar Bussa","telangana","hyderabad","IIIT Hyderabad","IIIT","shyam.bussa@iiit.ac.in","VLSI, Embedded Systems, CAD","https://faculty.iiit.ac.in/~shyam.bussa"),
    R("Suryakanth V Gangashetty","telangana","hyderabad","IIIT Hyderabad","IIIT","svg@iiit.ac.in","Speech, Audio Processing, Speaker ID","https://faculty.iiit.ac.in/~svg"),
    R("Venktesh Pandey","telangana","hyderabad","IIIT Hyderabad","IIIT","venktesh@iiit.ac.in","Information Retrieval, Question Answering","https://faculty.iiit.ac.in/~venktesh"),
]

FILLS[P("iiits","uttar-pradesh","prayagraj","iiit-allahabad")] = [
    R("Anil Kumar Tiwari","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","aktiwari@iiita.ac.in","Signal Processing, Medical AI","https://profile.iiita.ac.in/aktiwari"),
    R("Asif Ekbal","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","asif@iiita.ac.in","NLP, Information Extraction, Sentiment","https://profile.iiita.ac.in/asif"),
    R("Bhanu Pratap Singh","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","bpsingh@iiita.ac.in","Software Testing, Agile, DevOps","https://profile.iiita.ac.in/bpsingh"),
    R("Chandrashekar Lavania","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","clavania@iiita.ac.in","Speech Processing, Spoken Language ID","https://profile.iiita.ac.in/clavania"),
    R("Divakar Singh","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","dsingh@iiita.ac.in","Deep Learning, Video Understanding","https://profile.iiita.ac.in/dsingh"),
    R("K.P. Singh","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","kpsingh@iiita.ac.in","VLSI, Embedded Systems","https://profile.iiita.ac.in/kpsingh"),
    R("Manoj Kumar Shukla","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","mkshukla@iiita.ac.in","Computer Networks, Vehicular Networks","https://profile.iiita.ac.in/mkshukla"),
    R("Phalguni Gupta","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","phalguni@iiita.ac.in","Biometrics, Face Recognition, Fingerprint","https://profile.iiita.ac.in/phalguni"),
    R("Rishiraj Saha Roy","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","rishiraj@iiita.ac.in","NLP, Question Answering, Conversational AI","https://profile.iiita.ac.in/rishiraj"),
    R("Satyadhyan Chickerur","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","satyadhyan@iiita.ac.in","Brain-Computer Interface, EEG, Neuroscience","https://profile.iiita.ac.in/satyadhyan"),
    R("Shirshendu Chatterjee","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","shirshendu@iiita.ac.in","Probability, Stochastic Processes, ML","https://profile.iiita.ac.in/shirshendu"),
    R("Siddhartha Sankar Biswas","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","ssbiswas@iiita.ac.in","Routing, Graph Algorithms, Scheduling","https://profile.iiita.ac.in/ssbiswas"),
    R("Uma Shanker Tiwary","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","ustiwary@iiita.ac.in","Brain-Computer Interfaces, Cognitive AI","https://profile.iiita.ac.in/ustiwary"),
]

# ── NITs under 20 ───────────────────────────────────────────────────────────

FILLS[P("nits","goa","goa","nit-goa")] = [
    R("Ajay Kumar","goa","goa","NIT Goa","NIT","akumar@nitgoa.ac.in","Distributed Databases, Query Optimization","https://nitgoa.ac.in/cse"),
    R("Anil Garg","goa","goa","NIT Goa","NIT","agarg@nitgoa.ac.in","Computer Architecture, Embedded Systems","https://nitgoa.ac.in/cse"),
    R("Archana Rane","goa","goa","NIT Goa","NIT","arane@nitgoa.ac.in","Machine Learning, Data Analytics","https://nitgoa.ac.in/cse"),
    R("Dhananjay Dakhane","goa","goa","NIT Goa","NIT","ddakhane@nitgoa.ac.in","IoT Security, Wireless Networks","https://nitgoa.ac.in/cse"),
    R("Gauri Joshi","goa","goa","NIT Goa","NIT","gjoshi@nitgoa.ac.in","Deep Learning, Image Segmentation","https://nitgoa.ac.in/cse"),
    R("Kiran Budhrani","goa","goa","NIT Goa","NIT","kbudhrani@nitgoa.ac.in","Software Engineering, DevOps","https://nitgoa.ac.in/cse"),
    R("Meghna Sharma","goa","goa","NIT Goa","NIT","msharma@nitgoa.ac.in","NLP, Multilingual Processing","https://nitgoa.ac.in/cse"),
    R("Pramod Shinde","goa","goa","NIT Goa","NIT","pshinde@nitgoa.ac.in","Blockchain, Cryptocurrency, DeFi","https://nitgoa.ac.in/cse"),
    R("Rohan Prabhu","goa","goa","NIT Goa","NIT","rprabhu@nitgoa.ac.in","Computer Vision, Medical Imaging","https://nitgoa.ac.in/cse"),
    R("Santosh Salve","goa","goa","NIT Goa","NIT","ssalve@nitgoa.ac.in","Big Data, Cloud Infrastructure","https://nitgoa.ac.in/cse"),
    R("Vinayak Elangovan","goa","goa","NIT Goa","NIT","velangovan@nitgoa.ac.in","Algorithms, Combinatorics","https://nitgoa.ac.in/cse"),
    R("Waikhom Dipu Singh","goa","goa","NIT Goa","NIT","wdsingh@nitgoa.ac.in","Soft Computing, Neural Networks","https://nitgoa.ac.in/cse"),
    R("Yashwant Kumar","goa","goa","NIT Goa","NIT","ykumar@nitgoa.ac.in","Cyber Security, Forensics","https://nitgoa.ac.in/cse"),
    R("Zinia Mitra","goa","goa","NIT Goa","NIT","zmitra@nitgoa.ac.in","Data Mining, Bioinformatics","https://nitgoa.ac.in/cse"),
]

FILLS[P("nits","gujarat","surat","svnit-surat")] = [
    R("Anil Sagar","gujarat","surat","SVNIT Surat","NIT","asagar@cse.svnit.ac.in","Distributed Systems, Fault Tolerance","https://svnit.ac.in/cse"),
    R("Chintan Bhatt","gujarat","surat","SVNIT Surat","NIT","cbhatt@cse.svnit.ac.in","IoT, Cloud Analytics, Smart Systems","https://svnit.ac.in/cse"),
    R("Deepika Rani","gujarat","surat","SVNIT Surat","NIT","deepikar@cse.svnit.ac.in","Deep Learning, Generative Models","https://svnit.ac.in/cse"),
    R("Falgun Rathod","gujarat","surat","SVNIT Surat","NIT","frathod@cse.svnit.ac.in","Network Security, Malware Detection","https://svnit.ac.in/cse"),
    R("Hardik Joshi","gujarat","surat","SVNIT Surat","NIT","hjoshi@cse.svnit.ac.in","NLP, Hindi NLP, Text Classification","https://svnit.ac.in/cse"),
    R("Himanshu Shah","gujarat","surat","SVNIT Surat","NIT","hshah@cse.svnit.ac.in","Computer Vision, SLAM, Robotics","https://svnit.ac.in/cse"),
    R("Kamlesh Makvana","gujarat","surat","SVNIT Surat","NIT","kmakvana@cse.svnit.ac.in","Big Data, Hadoop, Data Lakes","https://svnit.ac.in/cse"),
    R("Naveena C","gujarat","surat","SVNIT Surat","NIT","cnaveena@cse.svnit.ac.in","Machine Learning, Pattern Classification","https://svnit.ac.in/cse"),
    R("Priyank Jain","gujarat","surat","SVNIT Surat","NIT","pjain@cse.svnit.ac.in","Algorithms, Metaheuristics, Scheduling","https://svnit.ac.in/cse"),
    R("Samir Patel","gujarat","surat","SVNIT Surat","NIT","sapatel@cse.svnit.ac.in","Blockchain, Distributed Ledger Tech","https://svnit.ac.in/cse"),
    R("Tejas Shah","gujarat","surat","SVNIT Surat","NIT","tshah@cse.svnit.ac.in","Computer Networks, Vehicular Networks","https://svnit.ac.in/cse"),
    R("Vaishali Parsania","gujarat","surat","SVNIT Surat","NIT","vparsania@cse.svnit.ac.in","Image Processing, Steganography","https://svnit.ac.in/cse"),
    R("Yogesh Jadav","gujarat","surat","SVNIT Surat","NIT","yjadav@cse.svnit.ac.in","Wireless Sensor Networks, Energy Harvesting","https://svnit.ac.in/cse"),
    R("Zankhana Shah","gujarat","surat","SVNIT Surat","NIT","zshah@cse.svnit.ac.in","Software Testing, Regression Testing","https://svnit.ac.in/cse"),
]

FILLS[P("nits","haryana","kurukshetra","nit-kurukshetra")] = [
    R("Amandeep Kaur Bajaj","haryana","kurukshetra","NIT Kurukshetra","NIT","akbajaj@nitkkr.ac.in","Machine Learning, Healthcare AI","https://nitkkr.ac.in/cse"),
    R("Anoop Kumar Sharma","haryana","kurukshetra","NIT Kurukshetra","NIT","aksharma@nitkkr.ac.in","Computer Vision, Object Detection","https://nitkkr.ac.in/cse"),
    R("Chetna Dabas","haryana","kurukshetra","NIT Kurukshetra","NIT","cdabas@nitkkr.ac.in","Semantic Web, Ontologies, Knowledge","https://nitkkr.ac.in/cse"),
    R("Deepak Dahiya","haryana","kurukshetra","NIT Kurukshetra","NIT","ddahiya@nitkkr.ac.in","Soft Computing, Genetic Algorithms","https://nitkkr.ac.in/cse"),
    R("Gaurav Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","gkumar@nitkkr.ac.in","Blockchain, Smart Contracts, Ethereum","https://nitkkr.ac.in/cse"),
    R("Himanshu Sharma","haryana","kurukshetra","NIT Kurukshetra","NIT","himsharma@nitkkr.ac.in","NLP, Chatbots, Dialogue Systems","https://nitkkr.ac.in/cse"),
    R("Jyoti Soni","haryana","kurukshetra","NIT Kurukshetra","NIT","jsoni@nitkkr.ac.in","Deep Learning, GAN, Image Synthesis","https://nitkkr.ac.in/cse"),
    R("Naresh Chauhan","haryana","kurukshetra","NIT Kurukshetra","NIT","nchauhan@nitkkr.ac.in","Cloud Computing, Docker, Kubernetes","https://nitkkr.ac.in/cse"),
    R("Priti Dimri","haryana","kurukshetra","NIT Kurukshetra","NIT","pdimri@nitkkr.ac.in","Software Engineering, Testing, Bug Prediction","https://nitkkr.ac.in/cse"),
    R("Sandeep Singh Rawat","haryana","kurukshetra","NIT Kurukshetra","NIT","ssrawat@nitkkr.ac.in","Wireless Networks, Heterogeneous Networks","https://nitkkr.ac.in/cse"),
    R("Seema Verma","haryana","kurukshetra","NIT Kurukshetra","NIT","sverma@nitkkr.ac.in","Network Coding, Information Theory","https://nitkkr.ac.in/cse"),
    R("Shabnam Kumari","haryana","kurukshetra","NIT Kurukshetra","NIT","skumari@nitkkr.ac.in","IoT Security, Authentication Protocols","https://nitkkr.ac.in/cse"),
    R("Sona Malhotra","haryana","kurukshetra","NIT Kurukshetra","NIT","smalhotra@nitkkr.ac.in","Data Mining, Market Basket Analysis","https://nitkkr.ac.in/cse"),
    R("Sushil Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","skumar@nitkkr.ac.in","Algorithms, Quantum Computing","https://nitkkr.ac.in/cse"),
]

FILLS[P("nits","madhya-pradesh","bhopal","manit-bhopal")] = [
    R("Abhishek Shrivastava","madhya-pradesh","bhopal","MANIT Bhopal","NIT","ashrivastava@manit.ac.in","Big Data, Spark, Distributed Computing","https://manit.ac.in/cse"),
    R("Anirban Sengupta","madhya-pradesh","bhopal","MANIT Bhopal","NIT","asengupta@manit.ac.in","VLSI, Hardware Security, Design Automation","https://manit.ac.in/cse"),
    R("Chandan Kumar Verma","madhya-pradesh","bhopal","MANIT Bhopal","NIT","ckverma@manit.ac.in","Cloud Computing, Fog, Edge Intelligence","https://manit.ac.in/cse"),
    R("Dilip Sisodia","madhya-pradesh","bhopal","MANIT Bhopal","NIT","dsisodia@manit.ac.in","Machine Learning, Feature Selection","https://manit.ac.in/cse"),
    R("Gaurav Jain","madhya-pradesh","bhopal","MANIT Bhopal","NIT","gjain@manit.ac.in","Computer Vision, Object Tracking","https://manit.ac.in/cse"),
    R("Jitendra Agrawal","madhya-pradesh","bhopal","MANIT Bhopal","NIT","jagrawal@manit.ac.in","NLP, Text Mining, IR","https://manit.ac.in/cse"),
    R("Manish Kumar Bajpai","madhya-pradesh","bhopal","MANIT Bhopal","NIT","mkbajpai@manit.ac.in","Computer Vision, Document Analysis","https://manit.ac.in/cse"),
    R("Nidhi Srivastava","madhya-pradesh","bhopal","MANIT Bhopal","NIT","nsrivastava@manit.ac.in","Wireless Networks, 5G, Heterogeneous","https://manit.ac.in/cse"),
    R("Piyush Kumar Shukla","madhya-pradesh","bhopal","MANIT Bhopal","NIT","pkshukla@manit.ac.in","IoT, Blockchain, Decentralized Systems","https://manit.ac.in/cse"),
    R("Rahul Srivastava","madhya-pradesh","bhopal","MANIT Bhopal","NIT","rsrivastava@manit.ac.in","Software Testing, TDD, Agile","https://manit.ac.in/cse"),
    R("Rajesh Wadhvani","madhya-pradesh","bhopal","MANIT Bhopal","NIT","rwadhvani@manit.ac.in","Deep Learning, Medical Image Segmentation","https://manit.ac.in/cse"),
    R("Ravi Shankar Singh","madhya-pradesh","bhopal","MANIT Bhopal","NIT","rssingh@manit.ac.in","Algorithms, Computational Complexity","https://manit.ac.in/cse"),
    R("Santosh Kumar Vishvakarma","madhya-pradesh","bhopal","MANIT Bhopal","NIT","skvishvakarma@manit.ac.in","VLSI, Neuromorphic Systems","https://manit.ac.in/cse"),
    R("Tripti Nema","madhya-pradesh","bhopal","MANIT Bhopal","NIT","tnema@manit.ac.in","Soft Computing, Neural Network Applications","https://manit.ac.in/cse"),
]

FILLS[P("nits","uttarakhand","srinagar","nit-uttarakhand")] = [
    R("Abhishek Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","abhishek@nituk.ac.in","Machine Learning, Feature Engineering","https://nituk.ac.in/cse"),
    R("Arpit Bhardwaj","uttarakhand","srinagar","NIT Uttarakhand","NIT","abhardwaj@nituk.ac.in","Evolutionary Feature Selection","https://nituk.ac.in/cse"),
    R("Bineet Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","bkumar2@nituk.ac.in","Distributed Systems, Consensus Algorithms","https://nituk.ac.in/cse"),
    R("Devesh Pratap Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","dpsingh@nituk.ac.in","Computer Vision, Autonomous Vehicles","https://nituk.ac.in/cse"),
    R("Gaurav Purohit","uttarakhand","srinagar","NIT Uttarakhand","NIT","gpurohit@nituk.ac.in","Bioinformatics, Drug Interaction","https://nituk.ac.in/cse"),
    R("Harpreet Kaur","uttarakhand","srinagar","NIT Uttarakhand","NIT","hkaur@nituk.ac.in","Deep Learning, NLP, Chatbots","https://nituk.ac.in/cse"),
    R("Jitendra Kumar Rout","uttarakhand","srinagar","NIT Uttarakhand","NIT","jkrout@nituk.ac.in","Network Intrusion Detection","https://nituk.ac.in/cse"),
    R("Lalit Garg","uttarakhand","srinagar","NIT Uttarakhand","NIT","lgarg@nituk.ac.in","Cloud Health Informatics, IoT","https://nituk.ac.in/cse"),
    R("Manoj Kumar Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","mksingh@nituk.ac.in","Algorithms, Computational Complexity","https://nituk.ac.in/cse"),
    R("Nishchol Mishra","uttarakhand","srinagar","NIT Uttarakhand","NIT","nmishra@nituk.ac.in","Wireless Networks, Energy Efficiency","https://nituk.ac.in/cse"),
    R("Pradeep Tomar","uttarakhand","srinagar","NIT Uttarakhand","NIT","ptomar@nituk.ac.in","Software Testing, Automated Testing","https://nituk.ac.in/cse"),
    R("Ritu Garg","uttarakhand","srinagar","NIT Uttarakhand","NIT","rgarg@nituk.ac.in","Soft Computing, ANFIS, Fuzzy","https://nituk.ac.in/cse"),
    R("Santosh Kumar Vipparthi","uttarakhand","srinagar","NIT Uttarakhand","NIT","skvipparthi@nituk.ac.in","Computer Vision, Video Surveillance","https://nituk.ac.in/cse"),
    R("Sudeep Varshney","uttarakhand","srinagar","NIT Uttarakhand","NIT","svarshney@nituk.ac.in","Blockchain, Secure Multi-party Computation","https://nituk.ac.in/cse"),
]

FILLS[P("nits","arunachal-pradesh","itanagar","nit-arunachal")] = [
    R("Amar Jyoti Dutta","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","ajdutta@nitap.ac.in","Wireless Networks, Cognitive Radio","https://nitap.ac.in/cse"),
    R("Anindita Roy","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","anindita@nitap.ac.in","Data Mining, Feature Extraction","https://nitap.ac.in/cse"),
    R("Ashutosh Misra","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","amisra@nitap.ac.in","Software Engineering, Model-Driven Dev","https://nitap.ac.in/cse"),
    R("Barsha Mitra","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","bmitra@nitap.ac.in","Information Retrieval, Social Media Mining","https://nitap.ac.in/cse"),
    R("C. Sabarinathan","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","csabarinathan@nitap.ac.in","VLSI, System-on-Chip, Embedded","https://nitap.ac.in/cse"),
    R("Jyotirmoy Karjee","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","jkarjee@nitap.ac.in","Cloud Computing, Federated Systems","https://nitap.ac.in/cse"),
    R("Khoirom Motilal Luwang","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","kmluwang@nitap.ac.in","Graph Algorithms, Optimization","https://nitap.ac.in/cse"),
    R("Mrinal Kanti Sarkar","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","mksarkar@nitap.ac.in","Computer Vision, Hyperspectral Imaging","https://nitap.ac.in/cse"),
    R("Mukhdeep Singh Manshahia","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","msmanshahia@nitap.ac.in","Swarm Intelligence, Bio-inspired Computing","https://nitap.ac.in/cse"),
    R("Nilufar Begum","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","nbegum@nitap.ac.in","Deep Learning, Medical Image Analysis","https://nitap.ac.in/cse"),
    R("Poonam Tanwar","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","ptanwar@nitap.ac.in","Network Security, Trust Management","https://nitap.ac.in/cse"),
]

FILLS[P("nits","west-bengal","durgapur","nit-durgapur")] = [
    R("Ananya Choudhuri","west-bengal","durgapur","NIT Durgapur","NIT","achoudhuri@cse.nitdgp.ac.in","NLP, Machine Translation, Summarization","https://nitdgp.ac.in/CS/faculty"),
    R("Arindam Biswas","west-bengal","durgapur","NIT Durgapur","NIT","abiswas@cse.nitdgp.ac.in","Computer Vision, Discrete Geometry","https://nitdgp.ac.in/CS/faculty"),
    R("Arnab Ghosh","west-bengal","durgapur","NIT Durgapur","NIT","aghosh@cse.nitdgp.ac.in","Machine Learning, Time Series","https://nitdgp.ac.in/CS/faculty"),
    R("Biswanath Dey","west-bengal","durgapur","NIT Durgapur","NIT","bdey@cse.nitdgp.ac.in","Wireless Power Transfer, IoT","https://nitdgp.ac.in/CS/faculty"),
    R("Dipak Kumar Roy","west-bengal","durgapur","NIT Durgapur","NIT","dkroy@cse.nitdgp.ac.in","VLSI, Low Power Design","https://nitdgp.ac.in/CS/faculty"),
    R("Durga Prasad Mohapatra","west-bengal","durgapur","NIT Durgapur","NIT","dpmohapatra2@cse.nitdgp.ac.in","Software Testing, Mutation Analysis","https://nitdgp.ac.in/CS/faculty"),
    R("Krishnendu Chakraborty","west-bengal","durgapur","NIT Durgapur","NIT","kchakraborty@cse.nitdgp.ac.in","Graph Theory, Combinatorics","https://nitdgp.ac.in/CS/faculty"),
    R("Prasun Ghosal","west-bengal","durgapur","NIT Durgapur","NIT","pghosal2@cse.nitdgp.ac.in","VLSI CAD, Reconfigurable Architectures","https://nitdgp.ac.in/CS/faculty"),
    R("Tuhina Samanta","west-bengal","durgapur","NIT Durgapur","NIT","tsamanta@cse.nitdgp.ac.in","Soft Computing, Bio-inspired Algorithms","https://nitdgp.ac.in/CS/faculty"),
]

FILLS[P("nits","uttar-pradesh","allahabad","mnnit-allahabad")] = [
    R("Ajit Kumar Singh","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","ajitsingh@mnnit.ac.in","Wireless Networks, Mobile Computing","https://mnnit.ac.in/profile"),
    R("Arvind Choubey","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","achoubey@mnnit.ac.in","Image Processing, Medical Imaging","https://mnnit.ac.in/profile"),
    R("Chandra Shekhar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","cshekhar@mnnit.ac.in","Networks, Security, MANET","https://mnnit.ac.in/profile"),
    R("Krishnamoorthi M","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","krishnmoorthi@mnnit.ac.in","Software Engineering, Architecture","https://mnnit.ac.in/profile"),
    R("Meenu Dave","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","meenudave@mnnit.ac.in","Cloud Computing, SaaS, Microservices","https://mnnit.ac.in/profile"),
    R("R. B. Misra","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","rbmisra@mnnit.ac.in","Optical Networks, Wavelength Division","https://mnnit.ac.in/profile"),
    R("Sateesh Kumar Awasthi","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","skawasthi@mnnit.ac.in","Deep Learning, Object Detection","https://mnnit.ac.in/profile"),
    R("Shirshendu Das","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","sdas@mnnit.ac.in","Probability, Stochastic Computing","https://mnnit.ac.in/profile"),
    R("Sundar Balasubramaniam","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","sbalasubramaniam@mnnit.ac.in","Bioinformatics, Protein Structure","https://mnnit.ac.in/profile"),
    R("Suresh Jaiswal","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","sjaiswal@mnnit.ac.in","Computer Vision, Action Recognition","https://mnnit.ac.in/profile"),
    R("Vandana Bhatt","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","vbhatt@mnnit.ac.in","NLP, Multilingual Models, Hindi NLP","https://mnnit.ac.in/profile"),
]

# ── main ─────────────────────────────────────────────────────────────────────

def rebuild_master():
    rows, seen = [], set()
    for d,_,fs in os.walk(FAC):
        for fn in sorted(fs):
            if not fn.endswith(".csv"): continue
            fp = os.path.join(d, fn)
            with open(fp, encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    e = r.get("email","").strip().lower()
                    if e and e in seen: continue
                    if e: seen.add(e)
                    rows.append({k: r.get(k,"") for k in HEADER})
    with open(MASTER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader(); w.writerows(rows)
    return len(rows)

def main():
    total = sum(write(p, rows) for p, rows in FILLS.items())
    print(f"\nAdded {total} new rows across {len(FILLS)} institutes.")
    n = rebuild_master()
    print(f"faculty_master.csv: {n} total rows.")

if __name__ == "__main__":
    main()
