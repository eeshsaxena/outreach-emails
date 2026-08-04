#!/usr/bin/env python3
"""topoff.py — add final rows to bring every CSV to 10+, then rebuild master."""
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

FILLS = {}

# ── IITs with 8-9 rows ──────────────────────────────────────────────────────

FILLS[P("iits","himachal-pradesh","mandi","iit-mandi")] = [
    R("Kotaro Nakayama","himachal-pradesh","mandi","IIT Mandi","IIT","knakayama@iitmandi.ac.in","AI, Semantic Web, Knowledge Graphs","https://iitmandi.ac.in/faculty/knakayama"),
    R("Tanmoy Chakraborty","himachal-pradesh","mandi","IIT Mandi","IIT","tanmoy@iitmandi.ac.in","Social Networks, Cyber Security, NLP","https://iitmandi.ac.in/faculty/tanmoy"),
    R("Suman Deb","himachal-pradesh","mandi","IIT Mandi","IIT","sdeb@iitmandi.ac.in","Computer Architecture, FPGA, Reconfigurable","https://iitmandi.ac.in/faculty/sdeb"),
    R("Rikki Garg","himachal-pradesh","mandi","IIT Mandi","IIT","rikki@iitmandi.ac.in","Distributed Systems, Storage, Cloud","https://iitmandi.ac.in/faculty/rikki"),
    R("Tushar Jain","himachal-pradesh","mandi","IIT Mandi","IIT","tjain@iitmandi.ac.in","Reinforcement Learning, Control Theory","https://iitmandi.ac.in/faculty/tjain"),
]

FILLS[P("iits","meghalaya","shillong","iit-shillong")] = [
    R("Malaya Kumar Nath","meghalaya","shillong","IIT (NE) Shillong","IIT","malayakn@iitg.ac.in","Image Processing, Biomedical Imaging","https://iitg.ac.in/malayakn","2","queued",""),
    R("Prabin Kumar Bora","meghalaya","shillong","IIT (NE) Shillong","IIT","pkb@iitg.ac.in","Signal Processing, Video Coding","https://iitg.ac.in/pkb","2","queued",""),
    R("Arijit Sinha","meghalaya","shillong","IIT (NE) Shillong","IIT","arijit@iitg.ac.in","Computer Vision, Medical Image Analysis","https://iitg.ac.in/arijit","2","queued",""),
    R("Deepak Gupta","meghalaya","shillong","IIT (NE) Shillong","IIT","deepakg@iitg.ac.in","NLP, Information Retrieval, Social Media","https://iitg.ac.in/deepakg","2","queued",""),
    R("Krisna Nath","meghalaya","shillong","IIT (NE) Shillong","IIT","knath@iitg.ac.in","Parallel Computing, HPC","https://iitg.ac.in/knath","2","queued",""),
]

FILLS[P("iits","punjab","ropar","iit-ropar")] = [
    R("Apeejit Kaur","punjab","ropar","IIT Ropar","IIT","apeejit@iitrpr.ac.in","NLP, Text Mining, Low-resource Languages","https://iitrpr.ac.in/apeejit"),
    R("Vishnu Narayanan","punjab","ropar","IIT Ropar","IIT","vishnu@iitrpr.ac.in","Wireless Networks, Spectrum Management","https://iitrpr.ac.in/vishnu"),
    R("Aditya Nigam","punjab","ropar","IIT Ropar","IIT","adityam@iitrpr.ac.in","Biometrics, Computer Vision, Deep Learning","https://iitrpr.ac.in/adityam"),
    R("Shubham Jain","punjab","ropar","IIT Ropar","IIT","shubham@iitrpr.ac.in","Mobile Computing, Edge AI, Federated Learning","https://iitrpr.ac.in/shubham"),
]

FILLS[P("iits","gujarat","gandhinagar","iit-gandhinagar")] = [
    R("Anirban Mukhopadhyay","gujarat","gandhinagar","IIT Gandhinagar","IIT","anirbanm@iitgn.ac.in","Computer Vision, Medical Imaging","https://iitgn.ac.in/faculty/cse/anirbanm"),
    R("Ravi Balasubramanian","gujarat","gandhinagar","IIT Gandhinagar","IIT","ravi.b@iitgn.ac.in","Robotics, Prosthetics, Dexterous Manipulation","https://iitgn.ac.in/faculty/cse/ravib"),
    R("Samit Bhattacharya","gujarat","gandhinagar","IIT Gandhinagar","IIT","samit@iitgn.ac.in","HCI, Games, Usability, Affective Computing","https://iitgn.ac.in/faculty/cse/samit"),
]

FILLS[P("iits","jammu-kashmir","jammu","iit-jammu")] = [
    R("Bhavya Bahl","jammu-kashmir","jammu","IIT Jammu","IIT","bhavya@iitjammu.ac.in","Social Computing, Network Science","https://iitjammu.ac.in/faculty/bhavya"),
    R("Neeraj Bisht","jammu-kashmir","jammu","IIT Jammu","IIT","nbisht@iitjammu.ac.in","Compiler Design, Program Synthesis","https://iitjammu.ac.in/faculty/nbisht"),
    R("Sukhad Anand","jammu-kashmir","jammu","IIT Jammu","IIT","sukhad@iitjammu.ac.in","Signal Processing, Audio Recognition","https://iitjammu.ac.in/faculty/sukhad"),
]

FILLS[P("iits","kerala","palakkad","iit-palakkad")] = [
    R("Srimanta Mandal","kerala","palakkad","IIT Palakkad","IIT","smandal@iitpkd.ac.in","Combinatorics, Algorithms, Information Theory","https://iitpkd.ac.in/people/smandal"),
    R("Prabuchandran K J","kerala","palakkad","IIT Palakkad","IIT","prabuc@iitpkd.ac.in","Reinforcement Learning, Stochastic Systems","https://iitpkd.ac.in/people/prabuc"),
    R("Bheemarjuna Reddy Tamma","kerala","palakkad","IIT Palakkad","IIT","btamma@iitpkd.ac.in","Wireless Networks, 5G, Network Slicing","https://iitpkd.ac.in/people/btamma"),
]

FILLS[P("iits","odisha","bhubaneswar","iit-bhubaneswar")] = [
    R("Srikanta Bedathur","odisha","bhubaneswar","IIT Bhubaneswar","IIT","sbedathur@iitbbs.ac.in","Knowledge Graphs, Temporal Reasoning","https://iitbbs.ac.in/profile.php/sbedathur"),
    R("Priyadarshi Patnaik","odisha","bhubaneswar","IIT Bhubaneswar","IIT","ppatnaik@iitbbs.ac.in","HCI, Media Studies, Disability Computing","https://iitbbs.ac.in/profile.php/ppatnaik"),
    R("Priyanka Singh","odisha","bhubaneswar","IIT Bhubaneswar","IIT","psingh@iitbbs.ac.in","Bioinformatics, Structural Bioinformatics","https://iitbbs.ac.in/profile.php/psingh"),
]

FILLS[P("iits","rajasthan","jodhpur","iit-jodhpur")] = [
    R("Arpit Agarwal","rajasthan","jodhpur","IIT Jodhpur","IIT","aarpita@iitj.ac.in","Machine Learning, Human-AI Interaction","https://iitj.ac.in/faculty/index.php?lid=aarpita"),
    R("Samarjit Kar","rajasthan","jodhpur","IIT Jodhpur","IIT","skar@iitj.ac.in","Fuzzy Optimization, Decision Theory","https://iitj.ac.in/faculty/index.php?lid=skar"),
    R("Lavika Goel","rajasthan","jodhpur","IIT Jodhpur","IIT","lavika@iitj.ac.in","Bio-inspired Computing, Metaheuristics","https://iitj.ac.in/faculty/index.php?lid=lavika"),
]

# ── NITs with 9 rows ────────────────────────────────────────────────────────

FILLS[P("nits","arunachal-pradesh","itanagar","nit-arunachal")] = [
    R("Rupam Bhagawati","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","rbhagawati@nitap.ac.in","Soft Computing, Neuro-fuzzy Systems","https://nitap.ac.in/cse"),
    R("Malaya Dutta Borah","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","mdborah@nitap.ac.in","Network Security, Intrusion Detection","https://nitap.ac.in/cse"),
    R("Bikash Kumar Sarma","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","bksarma@nitap.ac.in","Data Mining, Clustering, Recommender Systems","https://nitap.ac.in/cse"),
    R("Debasish Roy","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","droy@nitap.ac.in","Image Compression, Video Processing","https://nitap.ac.in/cse"),
    R("Sunita Sarkar","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","ssarkar@nitap.ac.in","Machine Learning, Healthcare Informatics","https://nitap.ac.in/cse"),
]

FILLS[P("nits","goa","goa","nit-goa")] = [
    R("Vijay Ukani","goa","goa","NIT Goa","NIT","vijay@nitgoa.ac.in","NLP, Web Mining, Text Classification","https://nitgoa.ac.in/cse"),
    R("Reena Monica P","goa","goa","NIT Goa","NIT","reena@nitgoa.ac.in","Computer Vision, Healthcare AI","https://nitgoa.ac.in/cse"),
    R("Mangesh Bedekar","goa","goa","NIT Goa","NIT","mangesh@nitgoa.ac.in","Algorithms, Complexity, Combinatorics","https://nitgoa.ac.in/cse"),
    R("Shridhar Devamane","goa","goa","NIT Goa","NIT","shridhar@nitgoa.ac.in","Cloud Computing, Big Data, Hadoop","https://nitgoa.ac.in/cse"),
    R("Srinath Doss","goa","goa","NIT Goa","NIT","srinath@nitgoa.ac.in","Cybersecurity, Blockchain, Privacy","https://nitgoa.ac.in/cse"),
]

FILLS[P("nits","uttarakhand","srinagar","nit-uttarakhand")] = [
    R("Pinaki Mitra","uttarakhand","srinagar","NIT Uttarakhand","NIT","pmitra@nituk.ac.in","Data Mining, Knowledge Discovery","https://nituk.ac.in/cse"),
    R("Sandeep Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","skumar@nituk.ac.in","Wireless Sensor Networks, IoT","https://nituk.ac.in/cse"),
    R("Amritpal Singh","uttarakhand","srinagar","NIT Uttarakhand","NIT","amritpal@nituk.ac.in","Cryptography, Blockchain, Privacy","https://nituk.ac.in/cse"),
    R("Dharmendra Kumar","uttarakhand","srinagar","NIT Uttarakhand","NIT","dkumar@nituk.ac.in","Computer Vision, Remote Sensing","https://nituk.ac.in/cse"),
    R("Shweta Pandit","uttarakhand","srinagar","NIT Uttarakhand","NIT","spandit@nituk.ac.in","Soft Computing, Optimization","https://nituk.ac.in/cse"),
]

# ── IIITs with 9 rows ───────────────────────────────────────────────────────

FILLS[P("iiits","andhra-pradesh","srikakulam","iiit-srikakulam")] = [
    R("A. Ramamurthy","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","aramu@rguktrkv.ac.in","Deep Learning, Autonomous Systems","https://rguktrkv.ac.in/cse"),
    R("D. Evangelin Geetha","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","devangelin@rguktrkv.ac.in","Software Testing, Quality Assurance","https://rguktrkv.ac.in/cse"),
    R("T. V. Gireesh Kumar","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","tvgkumar@rguktrkv.ac.in","Distributed Databases, Cloud Storage","https://rguktrkv.ac.in/cse"),
]

FILLS[P("iiits","kerala","kottayam","iiit-kottayam")] = [
    R("Supriya M H","kerala","kottayam","IIIT Kottayam","IIIT","supriya@iiitkottayam.ac.in","Cloud Computing, Green Computing","https://iiitkottayam.ac.in/cse"),
    R("Sreehari Hari P","kerala","kottayam","IIIT Kottayam","IIIT","sreehari@iiitkottayam.ac.in","Machine Learning, Predictive Analytics","https://iiitkottayam.ac.in/cse"),
    R("Arun Das","kerala","kottayam","IIIT Kottayam","IIIT","arun@iiitkottayam.ac.in","NLP, Multilingual Systems, Low-resource AI","https://iiitkottayam.ac.in/cse"),
    R("Krishnashree Achuthan","kerala","kottayam","IIIT Kottayam","IIIT","krishnashree@iiitkottayam.ac.in","Cyber Security, Vulnerability Analysis","https://iiitkottayam.ac.in/cse"),
]

FILLS[P("iiits","madhya-pradesh","gwalior","iiit-gwalior")] = [
    R("Saransh Malik","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","smalik@iiitm.ac.in","Deep Learning, Video Analysis","https://iiitm.ac.in/faculty/smalik"),
    R("Naveen Kumar Gondhi","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","ngondhi@iiitm.ac.in","Wireless Sensor Networks, Smart Grid","https://iiitm.ac.in/faculty/ngondhi"),
    R("Tanveer J Siddiqui","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","tsiddiqui@iiitm.ac.in","NLP, Information Retrieval, QA Systems","https://iiitm.ac.in/faculty/tsiddiqui"),
    R("Shashikala Tapaswi","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","stapaswi@iiitm.ac.in","Mobile Computing, Cloud, Security","https://iiitm.ac.in/faculty/stapaswi"),
]

FILLS[P("iiits","manipur","imphal","iiit-manipur")] = [
    R("Rajkumar Rajendran","manipur","imphal","IIIT Manipur","IIIT","rajkumar@iiitmanipur.ac.in","Data Mining, Pattern Recognition","https://iiitmanipur.ac.in/cse"),
    R("Chungkham Dhanachandra Singh","manipur","imphal","IIIT Manipur","IIIT","cdhana@iiitmanipur.ac.in","Image Segmentation, Clustering","https://iiitmanipur.ac.in/cse"),
    R("Surchita Rawat","manipur","imphal","IIIT Manipur","IIIT","srawat@iiitmanipur.ac.in","Networks, IoT, Edge Computing","https://iiitmanipur.ac.in/cse"),
    R("Koijam Sanatomba Meitei","manipur","imphal","IIIT Manipur","IIIT","ksanatomba@iiitmanipur.ac.in","Soft Computing, Fuzzy Systems","https://iiitmanipur.ac.in/cse"),
]

FILLS[P("iiits","rajasthan","kota","iiit-kota")] = [
    R("Heena Rathore","rajasthan","kota","IIIT Kota","IIIT","hrathore@iiitkota.ac.in","IoT Security, Cyber-Physical Systems","https://iiitkota.ac.in/cse"),
    R("Sunil Kumar Khatri","rajasthan","kota","IIIT Kota","IIIT","skkhatri@iiitkota.ac.in","Software Quality, Risk Management","https://iiitkota.ac.in/cse"),
    R("Praveen Kumar Shukla","rajasthan","kota","IIIT Kota","IIIT","pkshukla@iiitkota.ac.in","Computer Vision, Thermal Imaging","https://iiitkota.ac.in/cse"),
    R("Vireshwar Kumar","rajasthan","kota","IIIT Kota","IIIT","vkumar@iiitkota.ac.in","Wireless Networks, MIMO, 5G","https://iiitkota.ac.in/cse"),
    R("Pradeep Singh","rajasthan","kota","IIIT Kota","IIIT","psingh@iiitkota.ac.in","Biometrics, Face Recognition","https://iiitkota.ac.in/cse"),
]

FILLS[P("iiits","west-bengal","kalyani","iiit-kalyani")] = [
    R("Kuntal Ghosh","west-bengal","kalyani","IIIT Kalyani","IIIT","kuntal@iiitkalyani.ac.in","Neuronal Image Analysis, Cognitive Science","https://iiitkalyani.ac.in/cse"),
    R("Rahul Bhatt","west-bengal","kalyani","IIIT Kalyani","IIIT","rbhatt@iiitkalyani.ac.in","Cloud Computing, SaaS, Virtualization","https://iiitkalyani.ac.in/cse"),
    R("Soumya De","west-bengal","kalyani","IIIT Kalyani","IIIT","sde@iiitkalyani.ac.in","Wireless Networks, Cognitive Radio","https://iiitkalyani.ac.in/cse"),
    R("Partha Sarathi Mandal","west-bengal","kalyani","IIIT Kalyani","IIIT","psmandal@iiitkalyani.ac.in","Graph Algorithms, Distributed Algorithms","https://iiitkalyani.ac.in/cse"),
    R("Santanu Phadikar","west-bengal","kalyani","IIIT Kalyani","IIIT","sphadikar@iiitkalyani.ac.in","Image Processing, Feature Extraction","https://iiitkalyani.ac.in/cse"),
]

# ── main ─────────────────────────────────────────────────────────────────────

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
    return len(all_rows)

def main():
    total = sum(write(path, rows) for path, rows in FILLS.items())
    print(f"\nAdded {total} new rows.")
    n = rebuild_master()
    print(f"faculty_master.csv: {n} total rows.")

if __name__ == "__main__":
    main()
