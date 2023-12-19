#!/usr/bin/env python3
"""This module describes a function that returns the list of school having a specific topic
"""
def schools_by_topic(mongo_collection, topic):
    """Returns a List of school having a specific topic
    """
    result = mongo_collection.find(
            {"topics" : {"$in": [topic]}})
    return list(result)
