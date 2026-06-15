import pandas as pd
import random
from datetime import datetime, timedelta

def generate_cdr_file(filename, suspect_number, common_contacts, rows=500):
    """Generates a single CDR file for a specific suspect."""
    data = []
    start_date = datetime(2026, 6, 1)
    
    # A pool of random numbers unique to this suspect's log
    random_pool = [f"94123{random.randint(10000, 99999)}" for _ in range(30)]

    for _ in range(rows):
        current_date = start_date + timedelta(
            days=random.randint(0, 14), 
            hours=random.randint(0, 23), 
            minutes=random.randint(0, 59)
        )
        
        # 15% chance to call a common contact (the hidden link)
        if random.random() < 0.15:
            receiver = random.choice(common_contacts)
            duration = random.randint(45, 300)  # Meaningful conversations
        else:
            receiver = random.choice(random_pool)
            duration = random.randint(5, 600)

        data.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Time": current_date.strftime("%H:%M:%S"),
            "Caller_Number": suspect_number,
            "Receiver_Number": receiver,
            "Duration_Sec": duration,
            "Call_Type": random.choice(["Outgoing", "Incoming"]),
            "Tower_Location": random.choice(["Amroha Sector 2", "Joyo Road Close", "Gajraula Highway", "Kanth Crossroad"]),
            "IMEI": f"358912345678{random.randint(100, 999)}"
        })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Generated: {filename} ({rows} rows) for Suspect {suspect_number}")

if __name__ == "__main__":
    # These 3 numbers are the "links" or middlemen that BOTH suspects are calling secretly
    shared_middlemen = ["9000011111", "9000022222", "9555566666"]
    
    # Generate File 1 for Suspect A
    generate_cdr_file("suspect_1_cdr.csv", "9876543210", shared_middlemen, rows=600)
    
    # Generate File 2 for Suspect B
    generate_cdr_file("suspect_2_cdr.csv", "8877665544", shared_middlemen, rows=400)
    
    print("\n🚀 Ready! You now have 2 distinct files to upload together.")
