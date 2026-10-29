"""Generates a synthetic EV market dataset (data/ev_market.csv).
Replace with your own/official dataset if you have one; keep the same columns."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
mfr = {"Tesla":"USA","BYD":"China","Volkswagen":"Germany","Hyundai":"South Korea","Kia":"South Korea",
       "Tata Motors":"India","MG Motor":"UK","BMW":"Germany","Nissan":"Japan","Ford":"USA",
       "Rivian":"USA","NIO":"China","Mahindra":"India","Mercedes-Benz":"Germany","Volvo":"Sweden"}
cats = {"Hatchback":(35,300,22000,1.0),"Sedan":(60,480,42000,1.1),"SUV":(75,430,52000,1.4),
        "Bus":(250,260,180000,0.15),"Truck":(120,320,95000,0.25),"Two-Wheeler":(3,110,2500,2.5)}
batt = {"LFP":(0.3,-40),"NMC":(0.35,30),"NCA":(0.15,50),"Sodium-Ion":(0.08,-60),"Solid-State":(0.04,90)}
cw = np.array([v[3] for v in cats.values()]); cw = cw/cw.sum()
bw = np.array([v[0] for v in batt.values()]); bw = bw/bw.sum()
rows=[]
for i in range(600):
    m=str(rng.choice(list(mfr))); c=str(rng.choice(list(cats),p=cw)); b=str(rng.choice(list(batt),p=bw))
    cap,rkm,price,share=cats[c]; yr=int(rng.integers(2019,2026))
    cap=round(cap*rng.uniform(.85,1.2),1)
    rows.append(dict(Vehicle_ID=f"EV{i+1:04d}",Manufacturer=m,Model=f"{m.split()[0]}-{c[:3].upper()}{rng.integers(1,9)}",
        Category=c,Battery_Type=b,Battery_Capacity_kWh=cap,
        Range_km=max(40,int(rkm*rng.uniform(.85,1.2)+batt[b][1]+(yr-2019)*8)),
        Price_USD=int(price*rng.uniform(.8,1.3)),
        Annual_Sales=int(share*rng.lognormal(9.2,.8)*(1+(yr-2019)*.18)),
        Manufacturing_Country=mfr[m] if rng.random()<.7 else str(rng.choice(["China","Germany","USA","India","Japan","South Korea"])),
        Customer_Rating=round(float(np.clip(rng.normal(4.1,.5),2.5,5)),1),
        Charging_Time_Hrs=round(cap/rng.uniform(8,60)+rng.uniform(.3,1),1),Year=yr))
pd.DataFrame(rows).to_csv("data/ev_market.csv",index=False); print("ev_market.csv:",len(rows),"rows")
