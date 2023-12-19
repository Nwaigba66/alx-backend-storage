#!/usr/bin/env python3
"""This module describes a function that returns all students sorted by average score
"""
def top_students(mongo_collection):
    """The top must be ordered
     
     Returns with key = averageScore
     """

    # Sort students based on average score in descending order
    sorted_students = sorted(students, key=lambda x: x['averageScore'], reverse=True)

    return sorted_students
