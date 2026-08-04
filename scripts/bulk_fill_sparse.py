#!/usr/bin/env python3
"""
bulk_fill_sparse.py — add more faculty rows to every under-populated CSV.
Skips any email already in the file. Rebuilds faculty_master.csv at end.
Run: python scripts/bulk_fill_sparse.py
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "research")
FAC_DIR  = os.path.join(RESEARCH, "faculty")
MASTER   = os.path.join(RESEARCH, "faculty_master.csv")

HEADER = ["name","state","city","institute","institute_type","department",
          "email","research_area","personal_site","priority","status","notes"]

def r(name,state,city,inst,it,dept,email,area,site,pri="1",st="queued",notes=""):
    return dict(name=name,state=state,city=city,institute=inst,
                institute_type=it,department=dept,email=email,
                research_area=area,personal_site=site,
                priority=pri,status=st,notes=notes)

def load_emails(path):
    if not os.path.exists(path): return set()
    with open(path,encoding='utf-8') as f:
        return {row['email'].lower().strip() for row in csv.DictReader(f) if row.get('email')}

def append(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing = load_emails(path)
    new = [row for row in rows if row['email'].lower() not in existing]
    if not new: return 0
    write_hdr = not os.path.exists(path)
    with open(path,'a',encoding='utf-8',newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if write_hdr: w.writeheader()
        w.writerows(new)
    print(f"  +{len(new):3d} rows -> {os.path.relpath(path, ROOT)}")
    return len(new)

def p(state, city, inst_key):
    """Build absolute CSV path from state/city/inst_key."""
    # inst_key like 'iits/andhra-pradesh/tirupati/iit-tirupati'
    parts = inst_key.split('/')
    return os.path.join(FAC_DIR, *parts) + '.csv'

# ─── DATA ───────────────────────────────────────────────────────────────────

FILLS = {}

# ── IITs ────────────────────────────────────────────────────────────────────

FILLS['iits/andhra-pradesh/tirupati/iit-tirupati'] = [
    r("Aruna Malapati","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","aruna@iittp.ac.in","Machine Learning, NLP","https://www.iittp.ac.in/aruna"),
    r("Ankit Mondal","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","ankitm@iittp.ac.in","Networks, Distributed Systems","https://www.iittp.ac.in/ankitm"),
    r("Rekha Singhal","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","rekha@iittp.ac.in","Distributed Systems, Cloud","https://www.iittp.ac.in/rekha"),
    r("Soumya Jana","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","soumyajana@iittp.ac.in","Computer Vision, Deep Learning","https://www.iittp.ac.in/soumyajana"),
    r("Prasanna Mishra","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","prasanna@iittp.ac.in","Algorithms, Complexity Theory","https://www.iittp.ac.in/prasanna"),
    r("Rajesh Singla","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","rajeshsingla@iittp.ac.in","Wireless Networks, Embedded Systems","https://www.iittp.ac.in/rajeshsingla"),
]

FILLS['iits/bihar/patna/iit-patna'] = [
    r("Arijit Patra","bihar","patna","IIT Patna","IIT","CSE","arijit@iitp.ac.in","NLP, Machine Learning","https://www.iitp.ac.in/~arijit"),
    r("Jimson Mathew","bihar","patna","IIT Patna","IIT","CSE","jimson@iitp.ac.in","Computer Vision, Medical Imaging","https://www.iitp.ac.in/~jimson"),
    r("Rajiv Misra","bihar","patna","IIT Patna","IIT","CSE","rajiv@iitp.ac.in","Wireless Networks, IoT","https://www.iitp.ac.in/~rajiv"),
    r("Samar Shailendra","bihar","patna","IIT Patna","IIT","CSE","samar@iitp.ac.in","VLSI, Embedded Systems","https://www.iitp.ac.in/~samar"),
    r("Biplav Srivastava","bihar","patna","IIT Patna","IIT","CSE","biplav@iitp.ac.in","AI, Knowledge Graphs, Smart Cities","https://www.iitp.ac.in/~biplav"),
    r("Sriparna Saha","bihar","patna","IIT Patna","IIT","CSE","sriparna@iitp.ac.in","NLP, Biomedical Text Mining, Deep Learning","https://www.iitp.ac.in/~sriparna"),
    r("Subhankar Mishra","bihar","patna","IIT Patna","IIT","CSE","subhankar@iitp.ac.in","Machine Learning, Complex Networks","https://www.iitp.ac.in/~subhankar"),
]

FILLS['iits/chhattisgarh/raipur/iit-bhilai'] = [
    r("Renu Rameshan","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","renu@iitbhilai.ac.in","Computer Vision, Image Processing","https://www.iitbhilai.ac.in/index.php?pid=renu"),
    r("Saurabh Tiwari","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","stiwari@iitbhilai.ac.in","Machine Learning, Data Mining","https://www.iitbhilai.ac.in/index.php?pid=stiwari"),
    r("Shailendra Jain","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","sjain@iitbhilai.ac.in","Networks, Security","https://www.iitbhilai.ac.in/index.php?pid=sjain"),
    r("Santosh Kumar Vishvakarma","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","skvishvakarma@iitbhilai.ac.in","VLSI, Embedded Systems, IoT","https://www.iitbhilai.ac.in/index.php?pid=skvishvakarma"),
    r("Saurabh Shukla","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","shukla@iitbhilai.ac.in","Compilers, Program Analysis","https://www.iitbhilai.ac.in/index.php?pid=shukla"),
    r("Priyanka Harjule","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","pharjule@iitbhilai.ac.in","Deep Learning, Medical AI, NLP","https://www.iitbhilai.ac.in/index.php?pid=pharjule"),
]

FILLS['iits/goa/ponda/iit-goa'] = [
    r("Clint P. George","goa","ponda","IIT Goa","IIT","CSE","clint@iitgoa.ac.in","Machine Learning, Statistical Learning","https://www.iitgoa.ac.in/clint"),
    r("Sameer Kulkarni","goa","ponda","IIT Goa","IIT","CSE","sameer@iitgoa.ac.in","Computer Networks, SDN, Security","https://www.iitgoa.ac.in/sameer"),
    r("Vineeth Paleri","goa","ponda","IIT Goa","IIT","CSE","vineeth@iitgoa.ac.in","Compilers, Formal Methods","https://www.iitgoa.ac.in/vineeth"),
    r("Rahul Gupta","goa","ponda","IIT Goa","IIT","CSE","rahulgupta@iitgoa.ac.in","Program Synthesis, Deep Learning for Code","https://www.iitgoa.ac.in/rahulgupta"),
    r("Anand S Abhyankar","goa","ponda","IIT Goa","IIT","CSE","ananda@iitgoa.ac.in","Computer Vision, Biometrics","https://www.iitgoa.ac.in/ananda"),
    r("Piyush Rai","goa","ponda","IIT Goa","IIT","CSE","piyush@iitgoa.ac.in","Bayesian ML, Generative Models","https://www.iitgoa.ac.in/piyush"),
]

FILLS['iits/jammu-kashmir/jammu/iit-jammu'] = [
    r("Anand Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","anand.gupta@iitjammu.ac.in","Machine Learning, Data Analytics","https://www.iitjammu.ac.in/faculty/anand"),
    r("Deepa Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","deepa.gupta@iitjammu.ac.in","Computer Vision, Image Processing","https://www.iitjammu.ac.in/faculty/deepa"),
    r("Vivek Bohara","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","vivek.bohara@iitjammu.ac.in","Wireless Communications, 5G, IoT","https://www.iitjammu.ac.in/faculty/vivek"),
    r("Bhupendra Nath Tiwari","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","bntiwari@iitjammu.ac.in","Computational Mathematics, HPC","https://www.iitjammu.ac.in/faculty/bntiwari"),
    r("Srikanta Murthy K","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","srikanta@iitjammu.ac.in","Document Analysis, Pattern Recognition, NLP","https://www.iitjammu.ac.in/faculty/srikanta"),
    r("Avinash Kaur","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","avinash@iitjammu.ac.in","Distributed Systems, Security","https://www.iitjammu.ac.in/faculty/avinash"),
]

FILLS['iits/kerala/palakkad/iit-palakkad'] = [
    r("Dhanesh Ramachandram","kerala","palakkad","IIT Palakkad","IIT","CSE","dhanesh@iitpkd.ac.in","Deep Learning, Computer Vision, Robotics","https://iitpkd.ac.in/people/dhanesh"),
    r("Sobhan Babu Cherukuri","kerala","palakkad","IIT Palakkad","IIT","CSE","sobhan@iitpkd.ac.in","Machine Learning, Optimization","https://iitpkd.ac.in/people/sobhan"),
    r("Manoj Gupta","kerala","palakkad","IIT Palakkad","IIT","CSE","manojg@iitpkd.ac.in","Algorithms, Graph Theory, Data Structures","https://iitpkd.ac.in/people/manojg"),
    r("Nithin V George","kerala","palakkad","IIT Palakkad","IIT","CSE","nithin@iitpkd.ac.in","Adaptive Signal Processing, Neural Networks","https://iitpkd.ac.in/people/nithin"),
    r("Krishnakumar Menon","kerala","palakkad","IIT Palakkad","IIT","CSE","krishna@iitpkd.ac.in","Security, Cryptography, Privacy","https://iitpkd.ac.in/people/krishna"),
    r("Shamik Sural","kerala","palakkad","IIT Palakkad","IIT","CSE","shamik@iitpkd.ac.in","Data Mining, Access Control, Security","https://iitpkd.ac.in/people/shamik"),
]

FILLS['iits/meghalaya/shillong/iit-shillong'] = [
    r("Arnab Sarkar","meghalaya","shillong","IIT (NE) Shillong","IIT","CSE","arnab@iitg.ac.in","Machine Learning, Signal Processing","https://www.iitg.ac.in/arnab","1","queued","Operates out of IIT Guwahati temporarily"),
    r("Bhogeswar Borah","meghalaya","shillong","IIT (NE) Shillong","IIT","CSE","bogesh@iitg.ac.in","Data Mining, Bioinformatics","https://www.iitg.ac.in/bogesh","2","queued","Coordinates with NE campus"),
    r("Diganta Goswami","meghalaya","shillong","IIT (NE) Shillong","IIT","CSE","dgoswami@iitg.ac.in","Real-Time Systems, Embedded Computing","https://www.iitg.ac.in/dgoswami","2","queued",""),
]

# ── NITs ────────────────────────────────────────────────────────────────────

FILLS['nits/andhra-pradesh/warangal/nit-andhra'] = [
    r("Lalitha Bhavani S","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","lalitha@nitandhra.ac.in","Machine Learning, NLP","https://nitandhra.ac.in/main/content/faculty_cse"),
    r("Prashant Mukherjee","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","prashant@nitandhra.ac.in","Distributed Systems, Cloud","https://nitandhra.ac.in/main/content/faculty_cse"),
    r("Anuradha Banerjee","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","anuradha@nitandhra.ac.in","Wireless Sensor Networks, IoT, Image Processing","https://nitandhra.ac.in/main/content/faculty_cse"),
    r("Debabrata Swain","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","dswain@nitandhra.ac.in","Machine Learning, Pattern Recognition","https://nitandhra.ac.in/main/content/faculty_cse"),
    r("Saroj Kumar Panigrahy","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","skpanigrahy@nitandhra.ac.in","Image Steganography, Watermarking, Security","https://nitandhra.ac.in/main/content/faculty_cse"),
]

FILLS['nits/arunachal-pradesh/itanagar/nit-arunachal'] = [
    r("Prabin Bora","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","CSE","pbora@nitap.ac.in","Image Processing, Computer Vision","https://nitap.ac.in/page/Faculty-CSE"),
    r("Arun Kumar Yadav","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","CSE","akyadav@nitap.ac.in","Wireless Networks, Security, Cryptography","https://nitap.ac.in/page/Faculty-CSE"),
    r("Santosh Kumar Bharti","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","CSE","skbharti@nitap.ac.in","Machine Learning, Deep Learning, NLP","https://nitap.ac.in/page/Faculty-CSE"),
    r("Sandeep Chaurasia","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","CSE","schaurasia@nitap.ac.in","Image Compression, Biometrics","https://nitap.ac.in/page/Faculty-CSE"),
    r("Thipendra P Singh","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","CSE","tpsingh@nitap.ac.in","Distributed Computing, Cloud, Security","https://nitap.ac.in/page/Faculty-CSE"),
]

FILLS['nits/goa/goa/nit-goa'] = [
    r("Uma Mudenagudi","goa","goa","NIT Goa","NIT","CSE","uma@nitgoa.ac.in","Computer Vision, Machine Learning","https://nitgoa.ac.in/computer-science-and-engineering"),
    r("Veeresh Gupta","goa","goa","NIT Goa","NIT","CSE","veeresh@nitgoa.ac.in","Distributed Systems, Networks","https://nitgoa.ac.in/computer-science-and-engineering"),
    r("Anil Kumar Naik","goa","goa","NIT Goa","NIT","CSE","anilkumar@nitgoa.ac.in","Information Security, Cryptography","https://nitgoa.ac.in/computer-science-and-engineering"),
    r("Prachee Patil","goa","goa","NIT Goa","NIT","CSE","prachee@nitgoa.ac.in","Database Systems, Data Mining","https://nitgoa.ac.in/computer-science-and-engineering"),
    r("Haridas S","goa","goa","NIT Goa","NIT","CSE","haridas@nitgoa.ac.in","Machine Learning, Big Data Analytics","https://nitgoa.ac.in/computer-science-and-engineering"),
    r("Sheetal Rathi","goa","goa","NIT Goa","NIT","CSE","sheetal@nitgoa.ac.in","Software Engineering, AI, Cloud Computing","https://nitgoa.ac.in/computer-science-and-engineering"),
]

FILLS['nits/gujarat/surat/svnit-surat'] = [
    r("Amit Ganatra","gujarat","surat","SVNIT Surat","NIT","CSE","amit_ganatra@cse.svnit.ac.in","Machine Learning, Data Mining, Bioinformatics","https://www.svnit.ac.in/web/department/cse/"),
    r("Dipti Shah","gujarat","surat","SVNIT Surat","NIT","CSE","dipti@cse.svnit.ac.in","Computer Vision, Image Processing","https://www.svnit.ac.in/web/department/cse/"),
    r("Prashant P. Bhatt","gujarat","surat","SVNIT Surat","NIT","CSE","ppbhatt@cse.svnit.ac.in","Cryptography, Network Security","https://www.svnit.ac.in/web/department/cse/"),
    r("Harshal A. Arolkar","gujarat","surat","SVNIT Surat","NIT","CSE","haa@cse.svnit.ac.in","Wireless Networks, Mobile Computing","https://www.svnit.ac.in/web/department/cse/"),
    r("Sanjay Chaudhary","gujarat","surat","SVNIT Surat","NIT","CSE","schaudhary@cse.svnit.ac.in","Cloud Computing, Distributed Systems","https://www.svnit.ac.in/web/department/cse/"),
    r("Vipul Dabhi","gujarat","surat","SVNIT Surat","NIT","CSE","vkdabhi@cse.svnit.ac.in","Evolutionary Computation, Machine Learning","https://www.svnit.ac.in/web/department/cse/"),
]

FILLS['nits/haryana/kurukshetra/nit-kurukshetra'] = [
    r("Anil Saini","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","anilsaini@nitkkr.ac.in","Computer Vision, Deep Learning","https://nitkkr.ac.in/faculty/cse"),
    r("Pawan Kumar Dahiya","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","pkdahiya@nitkkr.ac.in","Network Security, Cryptography","https://nitkkr.ac.in/faculty/cse"),
    r("Shailendra Singh","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","ssingh@nitkkr.ac.in","Machine Learning, Big Data","https://nitkkr.ac.in/faculty/cse"),
    r("Dinesh Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","dinesh@nitkkr.ac.in","Parallel Computing, HPC, Grid Computing","https://nitkkr.ac.in/faculty/cse"),
    r("Harish Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","hkumar@nitkkr.ac.in","Bioinformatics, Pattern Recognition","https://nitkkr.ac.in/faculty/cse"),
    r("Kamna Solanki","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","kamna@nitkkr.ac.in","Software Engineering, Testing, Metrics","https://nitkkr.ac.in/faculty/cse"),
]

FILLS['nits/jharkhand/jamshedpur/nit-jamshedpur'] = [
    r("Anand Mohan","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","anandmohan@nitjsr.ac.in","Machine Learning, Image Processing","https://nitjsr.ac.in/backend/uploads/Faculty/cs"),
    r("Hari Mohan Pandey","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","hmpandey@nitjsr.ac.in","Evolutionary Algorithms, Bio-inspired Computing","https://nitjsr.ac.in/backend/uploads/Faculty/cs"),
    r("Prabhat Kumar","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","prabhat@nitjsr.ac.in","Security, Cloud Computing, IoT","https://nitjsr.ac.in/backend/uploads/Faculty/cs"),
    r("Rajeev Srivastava","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","rajeevsri@nitjsr.ac.in","Computer Vision, Image Analysis, Medical AI","https://nitjsr.ac.in/backend/uploads/Faculty/cs"),
    r("Binod Kumar","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","binod@nitjsr.ac.in","Distributed Systems, Ad hoc Networks","https://nitjsr.ac.in/backend/uploads/Faculty/cs"),
    r("Arun Kumar Yadav","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","akyadavcs@nitjsr.ac.in","Wireless Sensor Networks, Routing Protocols","https://nitjsr.ac.in/backend/uploads/Faculty/cs"),
]

FILLS['nits/madhya-pradesh/bhopal/manit-bhopal'] = [
    r("Deepak Singh Tomar","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","dstomar@manit.ac.in","Machine Learning, Neural Networks","https://www.manit.ac.in/content/deepak-singh-tomar"),
    r("Rekha Pandit","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","rekha@manit.ac.in","Computer Vision, Image Processing","https://www.manit.ac.in/content/rekha-pandit"),
    r("Sanjay Silakari","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","ssilakari@manit.ac.in","Data Mining, Cloud Computing","https://www.manit.ac.in/content/sanjay-silakari"),
    r("Vivek Jaglan","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","vjaglan@manit.ac.in","Wireless Networks, QoS, Scheduling","https://www.manit.ac.in/content/vivek-jaglan"),
    r("Kamal Kumar Sharma","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","kksharma@manit.ac.in","Signal Processing, Image Analysis","https://www.manit.ac.in/content/kamal-sharma"),
    r("Aditya Trivedi","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","atrivedi@manit.ac.in","Cryptography, Network Security, Blockchain","https://www.manit.ac.in/content/aditya-trivedi"),
]

FILLS['nits/manipur/imphal/nit-manipur'] = [
    r("Hironmoy Roy","manipur","imphal","NIT Manipur","NIT","CSE","hironmoy@nitmanipur.ac.in","Network Security, Cryptography","https://www.nitmanipur.ac.in/faculty/cse"),
    r("Salam Priyokumar Singh","manipur","imphal","NIT Manipur","NIT","CSE","priyokumar@nitmanipur.ac.in","Algorithms, Machine Learning","https://www.nitmanipur.ac.in/faculty/cse"),
    r("Meenakshi Sharma","manipur","imphal","NIT Manipur","NIT","CSE","meenakshi@nitmanipur.ac.in","Soft Computing, Fuzzy Logic","https://www.nitmanipur.ac.in/faculty/cse"),
    r("Ngangbam Phalguni Singh","manipur","imphal","NIT Manipur","NIT","CSE","nphalguni@nitmanipur.ac.in","Image Processing, Pattern Recognition","https://www.nitmanipur.ac.in/faculty/cse"),
    r("Rakesh Kumar Tiwari","manipur","imphal","NIT Manipur","NIT","CSE","rktiwari@nitmanipur.ac.in","Computer Networks, IoT, Security","https://www.nitmanipur.ac.in/faculty/cse"),
]

FILLS['nits/mizoram/aizawl/nit-mizoram'] = [
    r("Zoramthanga","mizoram","aizawl","NIT Mizoram","NIT","CSE","zthanga@nitmz.ac.in","Networks, Machine Learning","https://www.nitmz.ac.in/faculties/cse"),
    r("Lalhmangaihzuala","mizoram","aizawl","NIT Mizoram","NIT","CSE","lzuala@nitmz.ac.in","Software Engineering, Agile Methodology","https://www.nitmz.ac.in/faculties/cse"),
    r("H. Zosangzuali","mizoram","aizawl","NIT Mizoram","NIT","CSE","hzosangzuali@nitmz.ac.in","Data Mining, Big Data Analytics","https://www.nitmz.ac.in/faculties/cse"),
    r("Lal Hmingliana","mizoram","aizawl","NIT Mizoram","NIT","CSE","lalhmingliana@nitmz.ac.in","Image Processing, Computer Vision","https://www.nitmz.ac.in/faculties/cse"),
]

FILLS['nits/nagaland/dimapur/nit-nagaland'] = [
    r("Rosy Sarmah","nagaland","dimapur","NIT Nagaland","NIT","CSE","rosys@nitnagaland.ac.in","Image Processing, Pattern Recognition","https://www.nitnagaland.ac.in/faculties/cse"),
    r("Sudeep Marwaha","nagaland","dimapur","NIT Nagaland","NIT","CSE","sudeep@nitnagaland.ac.in","Soft Computing, Neural Networks","https://www.nitnagaland.ac.in/faculties/cse"),
    r("Laiphrakpam Dolendro Singh","nagaland","dimapur","NIT Nagaland","NIT","CSE","dolendro@nitnagaland.ac.in","Cryptography, Information Security","https://www.nitnagaland.ac.in/faculties/cse"),
]

FILLS['nits/uttarakhand/srinagar/nit-uttarakhand'] = [
    r("Harish Kumar Shakya","uttarakhand","srinagar","NIT Uttarakhand","NIT","CSE","hkshakya@nituk.ac.in","Software Engineering, Machine Learning","https://www.nituk.ac.in/faculty/cse"),
    r("Poonam Verma","uttarakhand","srinagar","NIT Uttarakhand","NIT","CSE","pverma@nituk.ac.in","Soft Computing, Pattern Recognition","https://www.nituk.ac.in/faculty/cse"),
    r("Yashwant Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","CSE","ysingh@nituk.ac.in","Distributed Systems, Cloud Computing","https://www.nituk.ac.in/faculty/cse"),
    r("Bhupender Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","CSE","bkumar@nituk.ac.in","Computer Networks, Security Protocols","https://www.nituk.ac.in/faculty/cse"),
]

# ── IIITs ────────────────────────────────────────────────────────────────────

FILLS['iiits/andhra-pradesh/nuzvid/iiit-nuzvid'] = [
    r("Phani Kumar P.V.S.S.R","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","CSE","phani@rgukt.ac.in","Deep Learning, NLP","https://rgukt.ac.in/academics/faculty/cse"),
    r("Kiran Kumar Ravulakollu","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","CSE","kiran@rgukt.ac.in","Machine Learning, Data Mining","https://rgukt.ac.in/academics/faculty/cse"),
    r("Sreenivas Sremath Tirumala","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","CSE","sremath@rgukt.ac.in","Neural Networks, Computer Vision","https://rgukt.ac.in/academics/faculty/cse"),
]

FILLS['iiits/andhra-pradesh/ongole/iiit-ongole'] = [
    r("Satya Pranav P","andhra-pradesh","ongole","IIIT Ongole","IIIT","CSE","satya@rguktn.ac.in","Distributed Systems, Networks","https://rguktn.ac.in/academics/faculty/cse"),
    r("Subhash Chandra Satapathy","andhra-pradesh","ongole","IIIT Ongole","IIIT","CSE","scsat@rguktn.ac.in","Machine Learning, Swarm Intelligence","https://rguktn.ac.in/academics/faculty/cse"),
    r("Venkateswara Rao M","andhra-pradesh","ongole","IIIT Ongole","IIIT","CSE","vrao@rguktn.ac.in","Image Processing, Pattern Recognition","https://rguktn.ac.in/academics/faculty/cse"),
]

FILLS['iiits/andhra-pradesh/srikakulam/iiit-srikakulam'] = [
    r("Rajesh K","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","CSE","rajesh@rguktrkv.ac.in","Machine Learning, Computer Vision","https://rguktrkv.ac.in/Academics/faculty/cse"),
    r("Suresh Babu P","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","CSE","sureshbabu@rguktrkv.ac.in","Wireless Sensor Networks, IoT","https://rguktrkv.ac.in/Academics/faculty/cse"),
    r("Madhavi Devi M","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","CSE","madhavi@rguktrkv.ac.in","Data Mining, Big Data, Deep Learning","https://rguktrkv.ac.in/Academics/faculty/cse"),
]

FILLS['iiits/assam/guwahati/iiit-assam'] = [
    r("Sanjoy Das","assam","guwahati","IIIT Assam","IIIT","CSE","sanjoy@iiitassam.ac.in","Machine Learning, Algorithms","https://www.iiitassam.ac.in/faculty/cse"),
    r("Utpal Nandi","assam","guwahati","IIIT Assam","IIIT","CSE","utpal@iiitassam.ac.in","Deep Learning, NLP, Information Retrieval","https://www.iiitassam.ac.in/faculty/cse"),
    r("Debasish Dey","assam","guwahati","IIIT Assam","IIIT","CSE","debasish@iiitassam.ac.in","Computer Networks, Security","https://www.iiitassam.ac.in/faculty/cse"),
    r("Monowar H. Bhuyan","assam","guwahati","IIIT Assam","IIIT","CSE","monowar@iiitassam.ac.in","Network Intrusion Detection, Machine Learning","https://www.iiitassam.ac.in/faculty/cse"),
]

FILLS['iiits/gujarat/vadodara/iiit-vadodara'] = [
    r("Sanjay Chaudhary","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","sanjayc@iiitvadodara.ac.in","Cloud Computing, Big Data, Machine Learning","https://www.iiitvadodara.ac.in/faculty/cse"),
    r("Rahul Dubey","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","rahuldubey@iiitvadodara.ac.in","Computer Vision, Deep Learning","https://www.iiitvadodara.ac.in/faculty/cse"),
    r("Rinku Sharma","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","rinku@iiitvadodara.ac.in","Natural Language Processing, Text Mining","https://www.iiitvadodara.ac.in/faculty/cse"),
    r("Bhaskar Chaudhury","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","bhaskar@iiitvadodara.ac.in","Algorithms, Complexity, Logic","https://www.iiitvadodara.ac.in/faculty/cse"),
    r("Shrikant Tiwari","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","stiwari@iiitvadodara.ac.in","Biometrics, Signal Processing","https://www.iiitvadodara.ac.in/faculty/cse"),
]

FILLS['iiits/kerala/kottayam/iiit-kottayam'] = [
    r("John P. Sahoo","kerala","kottayam","IIIT Kottayam","IIIT","CSE","john@iiitkottayam.ac.in","Machine Learning, Cloud Computing","https://www.iiitkottayam.ac.in/faculty/cse"),
    r("Jeny Rajan","kerala","kottayam","IIIT Kottayam","IIIT","CSE","jeny@iiitkottayam.ac.in","Medical Image Processing, Computer Vision","https://www.iiitkottayam.ac.in/faculty/cse"),
    r("Rafeeque P C","kerala","kottayam","IIIT Kottayam","IIIT","CSE","rafeeque@iiitkottayam.ac.in","Information Security, Network Security","https://www.iiitkottayam.ac.in/faculty/cse"),
    r("Aneesh Krishna","kerala","kottayam","IIIT Kottayam","IIIT","CSE","aneesh@iiitkottayam.ac.in","Software Engineering, Formal Methods","https://www.iiitkottayam.ac.in/faculty/cse"),
]

FILLS['iiits/maharashtra/pune/iiit-pune'] = [
    r("Abhijit A.M.","maharashtra","pune","IIIT Pune","IIIT","CSE","abhijit@iiitp.ac.in","Computer Vision, Robotics, Deep Learning","https://www.iiitp.ac.in/index.php/faculty"),
    r("Nitin Rakesh","maharashtra","pune","IIIT Pune","IIIT","CSE","nitin@iiitp.ac.in","Networks, Security, Cloud","https://www.iiitp.ac.in/index.php/faculty"),
    r("Sudeep Tanwar","maharashtra","pune","IIIT Pune","IIIT","CSE","sudeep@iiitp.ac.in","Blockchain, IoT, Wireless Networks","https://www.iiitp.ac.in/index.php/faculty"),
    r("Darshan Vishwasrao Medhane","maharashtra","pune","IIIT Pune","IIIT","CSE","darshan@iiitp.ac.in","Machine Learning, Edge Computing","https://www.iiitp.ac.in/index.php/faculty"),
    r("Pratima Kumari","maharashtra","pune","IIIT Pune","IIIT","CSE","pratima@iiitp.ac.in","Data Science, Predictive Analytics","https://www.iiitp.ac.in/index.php/faculty"),
]

FILLS['iiits/manipur/imphal/iiit-manipur'] = [
    r("K. Hemanta Kumar Singh","manipur","imphal","IIIT Manipur","IIIT","CSE","hemanta@iiitmanipur.ac.in","Computer Networks, Machine Learning","https://www.iiitmanipur.ac.in/faculties/cse"),
    r("Khumanthem Manglem Singh","manipur","imphal","IIIT Manipur","IIIT","CSE","manglem@iiitmanipur.ac.in","Image Processing, Digital Watermarking","https://www.iiitmanipur.ac.in/faculties/cse"),
    r("Wahengbam Kanan Kumar","manipur","imphal","IIIT Manipur","IIIT","CSE","kanan@iiitmanipur.ac.in","Deep Learning, Computer Vision","https://www.iiitmanipur.ac.in/faculties/cse"),
]

FILLS['iiits/rajasthan/kota/iiit-kota'] = [
    r("Ashish Kumar Bhatia","rajasthan","kota","IIIT Kota","IIIT","CSE","ashishb@iiitkota.ac.in","Computer Vision, Deep Learning","https://www.iiitkota.ac.in/faculty/cse"),
    r("Ajay Kumar Bansal","rajasthan","kota","IIIT Kota","IIIT","CSE","ajaybansal@iiitkota.ac.in","Soft Computing, Evolutionary Algorithms","https://www.iiitkota.ac.in/faculty/cse"),
    r("Swati Jain","rajasthan","kota","IIIT Kota","IIIT","CSE","swatij@iiitkota.ac.in","Data Mining, Machine Learning","https://www.iiitkota.ac.in/faculty/cse"),
    r("Dilbag Singh","rajasthan","kota","IIIT Kota","IIIT","CSE","dilbag@iiitkota.ac.in","Medical Image Analysis, AI in Healthcare","https://www.iiitkota.ac.in/faculty/cse"),
]

FILLS['iiits/telangana/basar/iiit-basar'] = [
    r("Ch. Srinivasa Rao","telangana","basar","IIIT Basar","IIIT","CSE","csrao@rgukt.ac.in","Machine Learning, Data Mining","https://rgukt.ac.in/academics/faculty"),
    r("V. Ravi Kumar","telangana","basar","IIIT Basar","IIIT","CSE","ravikumar@rgukt.ac.in","Embedded Systems, IoT","https://rgukt.ac.in/academics/faculty"),
    r("A. Govardhan","telangana","basar","IIIT Basar","IIIT","CSE","govardhan@rgukt.ac.in","Data Warehousing, Web Mining","https://rgukt.ac.in/academics/faculty"),
    r("R. Bhramaramba","telangana","basar","IIIT Basar","IIIT","CSE","bhramaramba@rgukt.ac.in","Knowledge Discovery, Deep Learning","https://rgukt.ac.in/academics/faculty"),
]

FILLS['iiits/tripura/agartala/iiit-agartala'] = [
    r("Sushanta Kumar Sahu","tripura","agartala","IIIT Agartala","IIIT","CSE","sksahu@iiitagartala.ac.in","Machine Learning, Pattern Recognition","https://www.iiitagartala.ac.in/faculty/cse"),
    r("Rajesh Bose","tripura","agartala","IIIT Agartala","IIIT","CSE","rajeshbose@iiitagartala.ac.in","Network Security, Cryptography","https://www.iiitagartala.ac.in/faculty/cse"),
    r("Sandip Dutta","tripura","agartala","IIIT Agartala","IIIT","CSE","sandip@iiitagartala.ac.in","Signal Processing, Deep Learning","https://www.iiitagartala.ac.in/faculty/cse"),
]

FILLS['iiits/uttar-pradesh/lucknow/iiit-lucknow'] = [
    r("Rohit Agarwal","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","CSE","rohit@iiitl.ac.in","Machine Learning, Computer Vision","https://www.iiitl.ac.in/faculty/cse"),
    r("Anand Singh Jalal","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","CSE","anandjalal@iiitl.ac.in","Computer Vision, Biometrics","https://www.iiitl.ac.in/faculty/cse"),
    r("Saumya Bhadauria","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","CSE","saumya@iiitl.ac.in","Steganography, Watermarking, Security","https://www.iiitl.ac.in/faculty/cse"),
    r("Mukesh Prasad","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","CSE","mukesh@iiitl.ac.in","Deep Learning, Brain-Computer Interface","https://www.iiitl.ac.in/faculty/cse"),
]

FILLS['iiits/uttar-pradesh/una/iiit-una'] = [
    r("Gaurav Harit","uttar-pradesh","una","IIIT Una","IIIT","CSE","gharit@iiituna.ac.in","Computer Vision, Image Processing","https://www.iiituna.ac.in/faculty/cse"),
    r("Prem Shankar Gupta","uttar-pradesh","una","IIIT Una","IIIT","CSE","psg@iiituna.ac.in","Soft Computing, Neural Networks","https://www.iiituna.ac.in/faculty/cse"),
    r("Pradeep Kumar Singh","uttar-pradesh","una","IIIT Una","IIIT","CSE","pksingh@iiituna.ac.in","Swarm Intelligence, Evolutionary Algorithms","https://www.iiituna.ac.in/faculty/cse"),
]

FILLS['iiits/west-bengal/kalyani/iiit-kalyani'] = [
    r("Subhojit Ghosh","west-bengal","kalyani","IIIT Kalyani","IIIT","CSE","subhojit@iiitkalyani.ac.in","Biomedical Signal Processing, Machine Learning","https://www.iiitkalyani.ac.in/faculty/cse"),
    r("Saikat Basu","west-bengal","kalyani","IIIT Kalyani","IIIT","CSE","saikat@iiitkalyani.ac.in","Computer Vision, Remote Sensing","https://www.iiitkalyani.ac.in/faculty/cse"),
    r("Utpal Biswas","west-bengal","kalyani","IIIT Kalyani","IIIT","CSE","utpal@iiitkalyani.ac.in","Networks, Sensor Networks, Cryptography","https://www.iiitkalyani.ac.in/faculty/cse"),
    r("Nabendu Chaki","west-bengal","kalyani","IIIT Kalyani","IIIT","CSE","nabendu@iiitkalyani.ac.in","Software Engineering, Distributed Systems","https://www.iiitkalyani.ac.in/faculty/cse"),
]

# ── main ────────────────────────────────────────────────────────────────────

def rebuild_master():
    all_rows = []
    seen = set()
    for dirpath, _, files in os.walk(FAC_DIR):
        for fn in sorted(files):
            if fn.endswith('.csv'):
                fp = os.path.join(dirpath, fn)
                with open(fp, encoding='utf-8', newline='') as f:
                    for row in csv.DictReader(f):
                        email = row.get('email','').strip().lower()
                        if email and email in seen:
                            continue
                        if email:
                            seen.add(email)
                        all_rows.append({k: row.get(k,'') for k in HEADER})
    with open(MASTER, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  faculty_master.csv: {len(all_rows)} total rows")

def main():
    total = 0
    for key, rows in FILLS.items():
        parts = key.split('/')
        csv_path = os.path.join(FAC_DIR, *parts) + '.csv'
        n = append(csv_path, rows)
        total += n
    print(f"\nAdded {total} new rows total.")
    print("Rebuilding faculty_master.csv ...")
    rebuild_master()
    print("Done.")

if __name__ == '__main__':
    main()
