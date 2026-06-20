from fastapi import FastAPI, HTTPException
import json 

app = FastAPI(title = "Fashion Store API", description = "Training API for Data Analysis.")

with open("database.json","r") as file:
    db = json.load(file)

@app.get("/")
def home():
    return {"message": "Store API is live. Navigate to /docs for interface"} 

@app.get("/api/buyers")
def get_all_buyers():
    return {"status": "success", "total_records": len(db), "data": db} 

@app.get("/api/buyers/{buyer_id}") 
def get_buyer(buyer_id: str):
    for buyer in db:
        if buyer["buyer_id"] == buyer_id:
            return {"status":"success", "data":buyer} 
             
@app.get("/api/buyers/filter/")
def filter_buyers(instagram_referred: bool = None, city : str=None):
    filtered_data = db 

    if instagram_referred is not None:
        filtered_data = [b for b in filtered_data if b["instagram_referred"] == instagram_referred]
    
    if city is not None:
        filtered_data = [b for b in filtered_data if b["city"].lower() == city.lower()]
    
    return {"status": "Success", "result_found": len(filtered_data), "data":filtered_data}

@app.get("/api/store/summary") 
def get_store_summary():
    total_revenue = sum(buyer["amount_spent"] for buyer in db)
    avg_rating = sum(buyer["rating_given"] for buyer in db) / len(db) 

    return {
        "status":"success",
        "data":{
            "total_revenue_usd": round(total_revenue, 2),
            "average_customer_rating":round(avg_rating, 2),
            "total_transactions": len(db)
        }
    }