#!/usr/bin/env python3
"""This module defines a function that updates all topics of a school document based on the name
"""

def update_topics(mongo_collection, name, topics):
    """Update topics of a school document
    """
    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
            );
