//Display the top 10 most frequent IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("Top 10 IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']} times")
