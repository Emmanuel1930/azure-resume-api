import azure.functions as func
import logging
import os
from azure.cosmos import CosmosClient, exceptions
from datetime import datetime
import json

# Environment variables
COSMOS_DB_ENDPOINT = os.environ['COSMOS_DB_ENDPOINT']
COSMOS_DB_KEY = os.environ['COSMOS_DB_KEY']
COSMOS_DB_DATABASE = os.environ['COSMOS_DB_DATABASE']
COSMOS_DB_CONTAINER = os.environ['COSMOS_DB_CONTAINER']

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
database = client.get_database_client(COSMOS_DB_DATABASE)
container = database.get_container_client(COSMOS_DB_CONTAINER)

# Function to get visitor count
def get_visitor_count():
    try:
        query = "SELECT c.visitorCount FROM c WHERE c.id = 'visitor_count'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        if items:
            return items[0].get('visitorCount', 0)
        return 0
    except Exception as e:
        logging.error(f'Error fetching visitor count: {str(e)}')
        return -1  # Return a specific value to indicate error

# Function to increment visitor count
def increment_visitor_count():
    try:
        query = "SELECT * FROM c WHERE c.id = 'visitor_count'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        if items:
            visitor_doc = items[0]
            visitor_doc['visitorCount'] += 1
            container.upsert_item(visitor_doc)
        else:
            container.upsert_item({"id": "visitor_count", "visitorCount": 1})
    except Exception as e:
        logging.error(f'Error incrementing visitor count: {str(e)}')

# Define the function app
app = func.FunctionApp()

@app.function_name("GetResumeData")
@app.route("getresumedata", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve query parameters
    resume_id = req.params.get('id')
    lang = req.params.get('lang')
    filter_by = req.params.get('filter')
    theme = req.params.get('theme')
    page = req.params.get('page')
    page_size = req.params.get('page_size')

    logging.info(f'Query parameters - ID: {resume_id}, Lang: {lang}, Filter: {filter_by}, Theme: {theme}, Page: {page}, Page Size: {page_size}')

      # Check if resume_id and lang are provided
    if not resume_id or not lang:
        # Return detailed instructions as the default response
        detailed_instructions = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emmanuel Resume</title>
    <style>
      /* Base styles */
body {
    font-family: Arial, sans-serif;
    background-color: #ffffff; /* Light mode background color */
    color: #1c1e21; /* Light mode text color */
    margin: 0;
    padding: 0;
    transition: background-color 0.3s, color 0.3s;
}

body.dark-mode {
    background-color: #1e1e1e; /* dark background color */
    color: #ffffff; /*dark text color */
}
/* Footer styles */
.footer {
    background-color: #333;
    color: #fff;
    padding: 10px 0; /* Reduced padding for mobile */
    text-align: center;
    font-family: Arial, sans-serif; /* Optional: Adjust font family */
}

.footer-content {
    max-width: 800px; /* Adjust max-width as needed */
    margin: 0 auto; /* Center content horizontally */
}

.footer h4 {
    font-size: 1rem; /* Reduced font size for mobile */
    margin: 0; /* Remove default margin */
    padding: 5px 0; /* Reduced padding around the text */
    line-height: 1.2; /* Adjusted line height for mobile */
}


/* Responsive adjustments */
@media (max-width: 768px) {
    .footer {
        padding: 8px 0; /* Adjusted padding for better spacing */
    }

    .footer h4 {
        font-size: 0.9rem; /* Further reduce font size for smaller screens */
        padding: 3px 0; /* Adjusted padding for better spacing */
    }
}


/* Styles for the hero area */
.hero_area {
    padding: 4rem 2rem; /* Adjust padding as needed */
    text-align: center; /* Center align content */
    background-color: #f9f9f9; /* Light theme background color */
    color: #333; /* Text color for light theme */
}

.hero_area.dark-mode {
    background-color: #1e1e1e; /* Dark theme background color */
    color: #ffffff; /* Text color for dark theme */
}

.hero_area img.profile-photo {
    width: 15rem; /* Adjust the size as per your preference */
    height: auto;
    border-radius: 50%; /* Create a circular shape */
    margin-bottom: 1.25rem; /* Space between photo and text */
    transition: transform 0.3s ease; /* Smooth transition for scaling */
}

.hero_area img.profile-photo:hover {
    transform: scale(1.1); /* Scale up to 110% on hover */
}

.hero_area h1 {
    margin-bottom: 1.25rem;
}

.hero_area p {
    margin-bottom: 1.875rem;
}

.hero_area .btn {
    background-color: #333;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem; /* Using rem units */
    text-decoration: none;
    font-size: 1rem; /* Using rem units */
    border-radius: 0.25rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.hero_area .btn:hover {
    background-color: #04aa6d; /* Accent color on hover */
}


.service_section .row {
    display: flex;
    flex-wrap: wrap; /* Allow items to wrap */
    justify-content: center; /* Center align items horizontally */
    gap: 40px; /* Gap between containers */
    /* padding: 40px 0; Remove padding to address blank space */
}

.service_section .col-md-6 {
    text-align: center; /* Center align text */
    width: calc(33.33% - 40px); /* Adjust width for responsiveness */
    margin: 20px; /* Adjust margin for spacing */
    background-color: #fff; /* Container background color */
    padding: 20px; /* Padding inside container */
    border-radius: 8px; /* Rounded corners */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Box shadow for depth */
    transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transitions */
}

.service_section .col-md-6:hover {
    transform: translateY(-5px); /* Lift container on hover */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Increased shadow on hover */
}

.service_section .col-md-6 img {
    width: 100%; /* Adjust image width */
    max-width: 150px; /* Limit max width */
    height: auto; /* Maintain aspect ratio */
    border-radius: 50%; /* Rounded image */
    display: block;
    margin: 0 auto 15px; /* Center image and add margin below */
    object-fit: cover; /* Ensure image covers container */
    border: 4px solid #fff; /* White border for contrast */
}

.service_section .text-center {
    padding: 0 15px;
}

.service_section p {
    margin: 10px 0; /* Adjust paragraph margin */
    font-size: 14px; /* Adjust font size */
    line-height: 1.5; /* Adjust line height for readability */
    color: #555; /* Text color */
    text-align: center; /* Center align text */
}

.service_section p::after {
    content: '';
    display: block;
    width: 20px;
    height: 2px;

    margin: 8px auto; /* Centered margin below text */
}

.service_section .btn {
    display: inline-block;
    padding: 8px 20px;
    margin-top: 10px;
    text-decoration: none;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    transition: background-color 0.3s;
    text-align: center; /* Center align button text */
}

.service_section .btn:hover {
    background-color: #0056b3;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
    .service_section .col-md-6 {
        width: calc(50% - 40px); /* 2 columns on larger desktop screens */
    }
}

@media (max-width: 768px) {
    .service_section .col-md-6 {
        width: calc(100% - 40px); /* 1 column on tablets and mobile */
    }

    .service_section .col-md-6 > div {
        padding: 20px; /* Adjust padding for content inside the box */
        margin-bottom: 20px; /* Space between stacked items */
    }
}

/* Small Round Button */
.small-round-button {
    position: fixed;
    top: 1.25rem;
    right: 1.25rem;
    width: 2.5rem; /* Using rem units */
    height: 2.5rem; /* Using rem units */
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.125rem; /* Using rem units */
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}

.small-round-button:hover {
    background-color: #04aa6d; /* Accent color on hover */
} 

.service_section.dark-mode .col-md-6 > div {
    background: #333; /* Dark container background effective */
}

.service_section.dark-mode .col-md-6:hover > div {
    background-color: #555; /* Dark grey hover effect */
}
.small-round-button.dark-mode {
    background-color: #04aa6d; /* Accent color */
    color: #1c1c1c; /* Light text */
}

.service_section.dark-mode .container,
.service_section.dark-mode .row,
.service_section.dark-mode .col-md-6 {
    background-color: #333; /* Dark container background effective */
    color: #f3f2ef; /* Dark text */
}

/* Styling for the "I am Emmanuel" heading */
h1 {
    font-size: 2.5rem; /* Adjust font size as needed */
    font-weight: 700; /* Bold font weight */
    color: var(--text-color); /* Default text color */
    margin-bottom: 20px;
    text-transform: uppercase; /* Uppercase text */
    letter-spacing: 1px; /* Letter spacing for emphasis */
    position: relative; /* Relative positioning for badge */
    display: inline-flex; /* Inline flex for alignment */
    align-items: center; /* Vertical alignment */
}

/* Styling for the verification badge */
h1::after {
    content: ""; /* Empty content for icon */
    width: 30px; /* Badge size */
    height: 30px; /* Badge size */
    background-image: url('https://media.istockphoto.com/id/1396933001/vector/vector-blue-verified-badge.jpg?s=612x612&w=0&k=20&c=aBJ2JAzbOfQpv2OCSr0k8kYe0XHutOGBAJuVjvWvPrQ='); /* Verification badge image URL */
    background-size: cover; /* Scale icon to cover dimensions */
    background-repeat: no-repeat; /* Prevent repetition */
    margin-left: 10px; /* Space between badge and text */
    position: relative; /* Relative positioning for badge */
    top: 5px; /* Adjust badge position */
    display: inline-block; /* Make badge display inline with text */
}

/* Styling for the description */
p {
    font-size: 1.1rem; /* Adjust font size as needed */
    line-height: 1.6; /* Line height for readability */
    color: var(--text-color); /* Default text color */
    margin-bottom: 20px;
}

/* Styling for the span element within the description */
:root {
    --badge-color: #0077b5; /* Define dark blue color for badge */
}

p span {
    color: var(--badge-color); /* Use CSS variable for badge color */
    font-weight: 700; /* Bold font weight */
}
/* Responsive adjustments */
@media only screen and (max-width: 768px) {
    h1 {
        font-size: 2rem; /* Decrease font size for tablets */
    }
    h1::after {
        width: 25px; /* Adjust badge size for tablets */
        height: 25px; /* Adjust badge size for tablets */
        margin-left: 8px; /* Adjust space between badge and text for tablets */
    }
}

@media only screen and (max-width: 480px) {
    h1 {
        font-size: 1.8rem; /* Further decrease font size for phones */
    }
    h1::after {
        width: 20px; /* Adjust badge size for phones */
        height: 20px; /* Adjust badge size for phones */
        margin-left: 6px; /* Adjust space between badge and text for phones */
    }
}
.social li a {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #333;
    color: #fff;
    transition: background-color 0.3s ease;
    text-decoration: none;
}

.social {
    list-style-type: none;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}

.social li {
    margin-right: 10px;
}

.social li a {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #333;
    color: #fff;
    transition: background-color 0.3s ease;
    text-decoration: none;
}

.social li a:hover {
    background-color: #555;
}

/* Specific styles for each social media link */
.social li.twitter a {
    background-color: #1DA1F2; /* Twitter blue */
}

.social li.linkedin a {
    background-color: #0077B5; /* LinkedIn blue */
}

.social li.instagram a {
    background-color: #C13584; /* Instagram pink */
}

.social li.github a {
    background-color: #333; /* GitHub black */
}

/* SVG styles */
.social li a svg {
    width: 60%;
    height: 60%;
    fill: #fff;
}

/* CSS for the acknowledgments section */
#acknowledgments {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 40px; /* Gap between containers */
    padding: 40px 0; /* Padding around the section */
    background-color: #f9f9f9; /* Light background color for the section */
    color: #555; /* Text color for light theme */
}

#acknowledgments.dark-mode {
    background-color: #1e1e1e; /* Dark background color for dark theme */
    color: #ffffff; /* Text color for dark theme */
}

#acknowledgments .container {
    position: relative;
    width: calc(33.33% - 40px); /* Adjust width for responsiveness */
    margin: 20px; /* Adjust margin for spacing */
    background-color: #ffffff; /* Lighter container background color */
    padding: 20px; /* Padding inside container */
    border-radius: 8px; /* Rounded corners */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Box shadow for depth */
    transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transitions */
    text-align: center; /* Center align content */
    display: flex; /* Ensure flex layout */
    flex-direction: column; /* Stack items vertically */
}

#acknowledgments.dark-mode .container {
    background-color: #2e2e2e; /* Darker container background color for dark theme */
}

#acknowledgments .container:hover {
    transform: translateY(-5px); /* Lift container on hover */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Increased shadow on hover */
}

#acknowledgments img {
    width: 100%; /* Adjust image width */
    max-width: 150px; /* Limit max width */
    height: auto; /* Maintain aspect ratio */
    border-radius: 50%; /* Rounded image */
    display: block;
    margin: 0 auto 15px; /* Center image and add margin below */
    object-fit: cover; /* Ensure image covers container */
    border: 4px solid #ffffff; /* Light border for contrast */
}

#acknowledgments.dark-mode img {
    border: 4px solid #2e2e2e; /* Dark border for contrast in dark theme */
}

#acknowledgments p {
    margin: 10px 0; /* Adjust paragraph margin */
    font-size: 14px; /* Adjust font size */
    line-height: 1.5; /* Adjust line height for readability */
}

#acknowledgments.dark-mode p {
    color: #ccc; /* Lighter text color for contrast in dark theme */
}

#acknowledgments .btn-group {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
}

#acknowledgments .btn-group .indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #ccc; /* Indicator color for light theme */
    margin: 0 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

#acknowledgments.dark-mode .btn-group .indicator {
    background-color: #888; /* Adjusted indicator color for dark theme */
}

#acknowledgments .btn-group .indicator.active {
    background-color: #007bff; /* Active indicator color */
}

#acknowledgments .container a {
    display: inline-block;
    padding: 8px 20px;
    margin-top: auto; /* Push links to the bottom */
    text-decoration: none;
    color: #ffffff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    transition: background-color 0.3s;
}

#acknowledgments .container a:hover {
    background-color: #0056b3;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
    #acknowledgments .container {
        width: calc(50% - 40px); /* 2 columns on larger desktop screens */
    }
}

@media (max-width: 768px) {
    #acknowledgments .container {
        width: calc(100% - 40px); /* 1 column on tablets and mobile */
    }
}
  /* Optional: Add CSS for active link styling */
  .navbar {
            background-color: #333;
            overflow: hidden;
        }
        .navbar a {
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            font-size: 17px;
        }
        .navbar a:hover {
            background-color: #ddd;
            color: black;
        }
        .navbar a.active {
            background-color: #04AA6D;
            color: white;
        }
        /* Optional: Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
/* Navbar styles */
.navbar {
    background-color: #333;
    overflow: hidden;
}

.navbar a {
    float: left;
    display: block;
    color: white;
    text-align: center;
    padding: 14px 20px;
    text-decoration: none;
    font-size: 17px;
}

.navbar a:hover {
    background-color: #ddd;
    color: black;
}

.navbar a.active {
    background-color: #6d7c77;
    color: white;
}

/* Hero Area styles effective*/
.hero_area {
    text-align: center;
    padding: 80px 20px;
    color: #333;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.hero_area img.profile-photo {
    width: 250px;
    height: auto;
    border-radius: 50%;
    margin-bottom: 20px;
    transition: transform 0.3s ease;
}

.hero_area img.profile-photo:hover {
    transform: scale(1.1);
}

.hero_area h1 {
    margin-bottom: 20px;
}

.hero_area p {
    margin-bottom: 30px;
}


.hero_area h1 {
    margin-bottom: 1.25rem;
}

.hero_area p {
    margin-bottom: 1.875rem;
}


.hero_area .btn:hover {
    background-color: #04aa6d; /* Accent color on hover for both themes */
}

.hero_area.dark-mode .btn {
    background-color: #0a66c2; /* Dark theme background color */
}

.hero_area.dark-mode .btn:hover {
    background-color: #1d9bd1; /* Dark theme accent color on hover  */
}


/* CSS for the service section new */
.service_section {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 40px; /* Gap between containers */
    padding: 40px 0; /* Padding around the section */
    background-color: #f9f9f9; /* Light background color for the section */
    color: #555; /* Text color for light theme */
    border-radius: 12px; /* Rounded corners for the section */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Soft shadow */
    overflow: hidden; /* Ensure shadow doesn't overflow */
}

.service_section.dark-mode {
    background-color: #1e1e1e; /* Dark background color for dark theme */
    color: #ffffff; /* Text color for dark theme */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); /* Darker shadow for dark theme */
}

.service_section .container {
    position: relative;
    width: calc(33.33% - 40px); /* Adjust width for responsiveness */
    margin: 20px; /* Adjust margin for spacing */
    background-color: #ffffff; /* Lighter container background color */
    padding: 20px; /* Padding inside container */
    border-radius: 8px; /* Rounded corners */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Box shadow for depth */
    transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transitions */
    text-align: center; /* Center align content */
    display: flex; /* Ensure flex layout */
    flex-direction: column; /* Stack items vertically */
}

.service_section.dark-mode .container {
    background-color: #2e2e2e; /* Darker container background color for dark theme */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Darker shadow for dark theme */
}

.service_section .container:hover {
    transform: translateY(-5px); /* Lift container on hover */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Increased shadow on hover */
}

.service_section img {
    width: 100%; /* Adjust image width */
    max-width: 150px; /* Limit max width */
    height: auto; /* Maintain aspect ratio */
    border-radius: 50%; /* Rounded image */
    display: block;
    margin: 0 auto 15px; /* Center image and add margin below */
    object-fit: cover; /* Ensure image covers container */
    border: 4px solid #ffffff; /* Light border for contrast */
    transition: transform 0.3s ease; /* Smooth image transition */
}

.service_section.dark-mode img {
    border: 4px solid #2e2e2e; /* Dark border for contrast in dark theme */
}

.service_section img:hover {
    transform: scale(1.05); /* Scale up image on hover */
}

.service_section p {
    margin: 10px 0; /* Adjust paragraph margin */
    font-size: 16px; /* Increased font size */
    line-height: 1.6; /* Adjusted line height for readability */
}

.service_section.dark-mode p {
    color: #ccc; /* Lighter text color for contrast in dark theme */
}

.service_section .btn-group {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
}

.service_section .btn-group .indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #ccc; /* Indicator color for light theme */
    margin: 0 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.service_section.dark-mode .btn-group .indicator {
    background-color: #888; /* Adjusted indicator color for dark theme */
}

.service_section .btn-group .indicator.active {
    background-color: #007bff; /* Active indicator color */
}

.service_section .container a {
    display: inline-block;
    padding: 10px 24px;
    margin-top: auto; /* Push links to the bottom */
    text-decoration: none;
    color: #ffffff;
    background-color: #007bff;
    border: none;
    border-radius: 6px;
    transition: background-color 0.3s, transform 0.2s;
}

.service_section .container a:hover {
    background-color: #0056b3;
    transform: translateY(-3px); /* Lift button on hover */
}
/* Gradient Overlay */
.service_section .container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}
/* Responsive adjustments */
@media (max-width: 1200px) {
    .service_section .container {
        width: calc(50% - 40px); /* 2 columns on larger desktop screens */
    }
}

@media (max-width: 768px) {
    .service_section .container {
        width: calc(100% - 40px); /* 1 column on tablets and mobile */
    }
}


/* Small Round Button */
.small-round-button {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 40px;
    height: 40px;
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}
.small-round-button:hover {
    background-color: #04aa6d;
}

/* Dark Mode Styles */
body.dark-mode {
    background-color: var(--background-color-dark);
    color: var(--text-color-dark);
}

.navbar.dark-mode {
    background-color: #fff; /* Light theme background color */
}

.navbar.dark-mode a.dark-mode {
    color: #1c1c1c; /* Dark theme text color */
}

.navbar a.active.dark-mode {
    background-color: #3e4914;
}

.hero_area.dark-mode {
    background-color: #444;
    color: var(--text-color-dark);
}

.hero_area .btn.dark-mode {
    background-color: #000000;
}

.hero_area.dark-mode {
    background-color: #1e1e1e; /* Matching dark background color */
    color: #ffffff; /* White text color */
}

.hero_area .btn.dark-mode {
    background-color: #0077b5; /*  blue button color */
    color: #ffffff; /* White text color */
}
.small-round-button.dark-mode {
    background-color: #0077b5; /* blue button color */
    color: #ffffff; /* White text color */
}
</style>
</head>
<body>
<!-- Navbar -->
<div class="navbar">
    <a href="#hero">Home</a>
    <a href="#acknowledgments">Recognition</a>
    <a href="#resume">Resume</a>
</div>
<!-- Hero Area -->
<div class="hero_area" id="hero">
    <img src="https://media.licdn.com/dms/image/D4E03AQEM6U3b39k-MQ/profile-displayphoto-shrink_800_800/0/1718211515117?e=1726099200&v=beta&t=KudN_sRlpo2jSag5KsLFCzJUXrEPPxlzJgI5QQ6oRB0" alt="Emmanuel's Photo" class="profile-photo">
    <h1>Hi, I'm Emmanuel</h1>
    <p>Visitor Count: <span id="visitorCount">Loading...</span></p>

    <!-- Social Media Links -->
    <ul class="social">
        <li class="twitter"><a href="https://twitter.com/oyeniyi-emmanuel"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M23.94 4.57c-.88.38-1.82.64-2.8.76 1.01-.6 1.78-1.54 2.15-2.67-.94.55-1.98.95-3.1 1.17-.89-.95-2.17-1.54-3.58-1.54-2.71 0-4.9 2.19-4.9 4.9 0 .38.04.75.13 1.1-4.08-.2-7.7-2.15-10.12-5.11-.42.72-.66 1.56-.66 2.45 0 1.7.86 3.19 2.17 4.07-.8 0-1.54-.25-2.2-.63v.06c0 2.37 1.68 4.34 3.92 4.78-.42.12-.87.18-1.33.18-.32 0-.64-.03-.95-.08.64 1.98 2.51 3.42 4.72 3.46-1.73 1.35-3.92 2.15-6.31 2.15-.41 0-.82-.02-1.23-.07 2.25 1.44 4.93 2.28 7.8 2.28 9.36 0 14.49-7.75 14.49-14.49 0-.22 0-.45-.02-.67.99-.71 1.85-1.6 2.54-2.61z"/></svg></a></li>
        <li class="linkedin"><a href="https://linkedin.com/in/oyeniyi-emmanuel"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 2H4C2.9 2 2.01 2.9 2.01 4L2 20c0 1.1.89 2 1.99 2H20c1.1 0 2-0.9 2-2V4c0-1.1-0.9-2-2-2zM8 18H5V9h3v9zM6.5 7.5c-0.83 0-1.5-0.67-1.5-1.5s0.67-1.5 1.5-1.5 1.5 0.67 1.5 1.5-0.67 1.5-1.5 1.5zM18 18h-2.99v-4.5c0-1.22-0.47-1.91-1.38-1.91-0.75 0-1.2 0.5-1.4 1h0V18h-3V9h2.98v1.2c0.36-0.55 1-1.2 2.3-1.2 1.68 0 3 1.09 3 3.42V18z"/></svg></a></li>
        <li class="instagram"><a href="https://instagram.com/oyeniyi-emmanuel"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.997 2.04c-2.722 0-3.056 0.011-4.122 0.06-1.064 0.048-1.79 0.217-2.426 0.463a4.901 4.901 0 0 0-1.771 1.151 4.898 4.898 0 0 0-1.152 1.77c-0.247 0.635-0.415 1.36-0.464 2.424C2.011 8.94 2 9.274 2 12s0.011 3.056 0.06 4.122c0.049 1.064 0.217 1.79 0.464 2.426a4.898 4.898 0 0 0 1.151 1.771 4.901 4.901 0 0 0 1.77 1.152c0.635 0.247 1.36 0.415 2.424 0.464 1.066 0.048 1.4 0.06 4.122 0.06s3.056-0.011 4.122-0.06c1.064-0.049 1.79-0.217 2.426-0.464a4.901 4.901 0 0 0 1.771-1.151 4.898 4.898 0 0 0 1.152-1.77c0.247-0.636 0.415-1.362 0.464-2.426 0.049-1.066 0.06-1.4 0.06-4.122s-0.011-3.056-0.06-4.122c-0.049-1.064-0.217-1.79-0.464-2.424a4.898 4.898 0 0 0-1.151-1.771 4.901 4.901 0 0 0-1.77-1.152c-0.636-0.247-1.362-0.415-2.426-0.464C15.053 2.011 14.719 2 11.997 2zM12 6.851c2.627 0 3.152 0.011 4.248 0.057 0.934 0.043 1.444 0.198 1.76 0.331 0.442 0.172 0.76 0.383 1.095 0.718 0.335 0.335 0.546 0.653 0.718 1.095 0.133 0.316 0.288 0.826 0.331 1.76 0.046 1.095 0.057 1.62 0.057 4.248s-0.011 3.152-0.057 4.248c-0.043 0.934-0.198 1.444-0.331 1.76-0.172 0.442-0.383 0.76-0.718 1.095-0.335 0.335-0.653 0.546-1.095 0.718-0.316 0.133-0.826 0.288-1.76 0.331-1.096 0.046-1.621 0.057-4.248 0.057s-3.152-0.011-4.248-0.057c-0.934-0.043-1.444-0.198-1.76-0.331-0.442-0.172-0.76-0.383-1.095-0.718-0.335-0.335-0.546-0.653-0.718-1.095-0.133-0.316-0.288-0.826-0.331-1.76-0.046-1.095-0.057-1.62-0.057-4.248s0.011-3.152 0.057-4.248c0.043-0.934 0.198-1.444 0.331-1.76 0.172-0.442 0.383-0.76 0.718-1.095 0.335-0.335 0.653-0.546 1.095-0.718 0.316-0.133 0.826-0.288 1.76-0.331 1.096-0.046 1.621-0.057 4.248-0.057zM12 9.943c-2.628 0-4.757 2.129-4.757 4.757s2.129 4.757 4.757 4.757 4.757-2.129 4.757-4.757-2.129-4.757-4.757-4.757zM12 17c-1.657 0-3-1.343-3-3s1.343-3 3-3 3 1.343 3 3-1.343 3-3 3z"/></svg></a></li>
        <li class="github"><a href="https://github.com/Emmanuel1930"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.17 6.839 9.491 0.5 0.092 0.682-0.218 0.682-0.482 0-0.238-0.009-0.868-0.014-1.705-2.782 0.602-3.368-1.34-3.368-1.34-0.454-1.154-1.11-1.463-1.11-1.463-0.908-0.621 0.068-0.607 0.068-0.607 1.004 0.071 1.531 1.032 1.531 1.032 0.891 1.527 2.338 1.086 2.911 0.831 0.091-0.646 0.349-1.086 0.634-1.336-2.22-0.253-4.555-1.107-4.555-4.931 0-1.089 0.39-1.982 1.032-2.682-0.104-0.253-0.447-1.268 0.098-2.644 0 0 0.837-0.268 2.743 1.024 0.796-0.221 1.649-0.331 2.497-0.335 0.848 0.004 1.701 0.114 2.497 0.335 1.906-1.292 2.742-1.024 2.742-1.024 0.547 1.376 0.204 2.391 0.1 2.644 0.645 0.7 1.03 1.593 1.03 2.682 0 3.834-2.339 4.674-4.565 4.922 0.36 0.308 0.681 0.918 0.681 1.849 0 1.335-0.012 2.412-0.012 2.74 0 0.267 0.18 0.577 0.688 0.479 3.97-1.322 6.832-5.075 6.832-9.49 0-5.523-4.477-10-10-10z"/></svg></a></li>
    </ul>

    <p>A student from Redeemer's University in Nigeria with a passion for Cloud Security.
        Welcome to my <span>Cloud Resume API Challenge</span>, where I'll be showcasing my skills in Azure.
        I'm excited to share my project with you, which now includes additional features that
        take my cloud resume to the next level.
    </p>
    
    <a href="#resume" class="btn">JSON Resume-focused project </a>
</div>

<section class="service_section">
    <div class="container" id="resume">
        <h2 class="text-center">Resume</h2>
        <p class="text-center">Additional Features of My JSON Resume</p>
        <div class="row">
            <div class="col-md-6">
                <div class="feature-item">
                    <h5>Resume ID and Language Selection (English)</h5>
                    <p>Access the resume in English by adding <code>?id=json&lang=en</code> to the URL.</p>
                    <a href="https://azureresumeapp.azurewebsites.net/api/getresumedata?id=json&lang=en" class="btn btn-primary">View in English <i class="fa fa-long-arrow-right" aria-hidden="true"></i></a>
                </div>
            </div>
            <div class="col-md-6">
                <div class="feature-item">
                    <h5>Resume ID and Language Selection (French)</h5>
                    <p>Access the resume in French by replacing <code>en</code> with <code>fr</code> in the URL: <code>?id=json&lang=fr</code></p>
                    <a href="https://azureresumeapp.azurewebsites.net/api/getresumedata?id=json&lang=fr" class="btn btn-primary">View in French <i class="fa fa-long-arrow-right" aria-hidden="true"></i></a>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="feature-item">
                    <h5>Condition Check: Verifies if the theme parameter matches 'minimal'</h5>
                    <p>Filtering Logic: When the theme is 'minimal', only the specified sections will be included.</p>
                    <a href="https://azureresumeapp.azurewebsites.net/api/getresumedata?id=json&lang=en&theme=minimal" class="btn btn-link">Learn more about minimal theme <i class="fa fa-long-arrow-right" aria-hidden="true"></i></a>
                </div>
            </div>
            <div class="col-md-6">
                <div class="feature-item">
                    <h5>Creating a Unique Theme: New theme parameter added</h5>
                    <p>Optimization of the current view, the use of the azure links, and even if it's a head.</p>
                    <a href="https://azureresumeapp.azurewebsites.net/api/getresumedata?id=json&lang=en&page=1&page_size=4" class="btn btn-link">Learn about themes <i class="fa fa-long-arrow-right" aria-hidden="true"></i></a>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- Acknowledgements SECTION -->
<section id="acknowledgments">
    <div class="container">
        <div class="heading-container">
            <h2>Acknowledgment</h2>
        </div>
        <img src="https://media.licdn.com/dms/image/D4D03AQHjPA4qXF_y3A/profile-displayphoto-shrink_800_800/0/1702391535993?e=1726099200&amp;v=beta&amp;t=raFd166JfF6qJ7gpVENkOQM5DHSQDIRRGQbDNNo3gAg" alt="Inspiration 1">
        <p>I extend my gratitude to Rishab Kumar for proposing the idea of building the Azure Resume API. 
            His initiative has made this project both challenging and rewarding.
        </p>
        <a href="https://www.linkedin.com/in/rishabkumar7/" target="_blank" class="btn">LinkedIn Profile</a>
    </div>

    <div class="container">
        <div class="heading-container">
            <h2>Acknowledgment</h2>
        </div>
        <img src="https://media.licdn.com/dms/image/D5603AQGkFSBgLveJLw/profile-displayphoto-shrink_200_200/0/1687909984859?e=1726099200&amp;v=beta&amp;t=Do3OFxEpt0plNSq-IGBbC3h2lP037RLrErPqaKZBN9s" alt="Inspiration 2" class="round-image">
        <p>I am grateful to Ifeanyi Otuonye for co-creating the Azure 
           Resume API project alongside Rishab Kumar.It has been an enriching experience.
        </p>
        <a href="https://www.linkedin.com/in/ifeanyi-otuonye/" target="_blank" class="btn">LinkedIn Profile</a>
    </div>

    <div class="container">
        <div class="heading-container">
            <h2>Acknowledgment</h2>
        </div>
        <img src="https://media.licdn.com/dms/image/D4E03AQESBZGLHHi8yg/profile-displayphoto-shrink_200_200/0/1714561859900?e=1726099200&amp;v=beta&amp;t=gu2lD6OFCGdowHP8IuVHr5qAmp-7J55NC-jM_pk5gx8" alt="Inspiration 3" class="round-image">
        <p>I also want to thank Gwyneth Peña for creating a comprehensive 6-month cloud security study plan. 
            This plan has significantly contributed to my skill development in this area.
        </p>
        <a href="https://www.linkedin.com/in/madebygps/" target="_blank" class="btn">LinkedIn Profile</a>
    </div>

    <div class="container">
        <div class="heading-container">
            <h2>Acknowledgment</h2>
        </div>
        <img src="https://avatars.githubusercontent.com/u/99533069?v=4" alt="Pelumi Adetoye">
        <p>I express my gratitude to Miss Pelz for her invaluable guidance and support throughout this project. 
           Her mentorship has been crucial in overcoming challenges and achieving progress.
        </p>
        <a href="https://www.linkedin.com/in/oluwapelumiadetoye/" target="_blank" class="btn">LinkedIn Profile</a>
    </div>

    <!-- Navigation indicators -->
    <div class="btn-group">
        <!-- Indicator buttons will be dynamically added here via JavaScript -->
    </div>
</section>

<!--footer section-->
<footer role="contentinfo" class="footer">
        <div class="footer">
            <h4> © 2024 Emmanuel Cloud Resume API with Azure</h4>
        </div>
</footer>


<!-- Small Round Button for Dark Mode Toggle -->
<button class="small-round-button" onclick="toggleDarkMode()">☀</button>


<!-- JavaScript for Dark Mode Toggle and Inspirations Slideshow -->
<script>
    // Dark Mode Toggle Function
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        document.querySelectorAll('.navbar').forEach(el => el.classList.toggle('dark-mode'));
        document.querySelectorAll('.navbar a').forEach(a => a.classList.toggle('dark-mode'));
        document.querySelector('.hero_area').classList.toggle('dark-mode');
        document.querySelector('.hero_area .btn').classList.toggle('dark-mode');
        document.querySelector('.service_section').classList.toggle('dark-mode');
        document.querySelectorAll('.service_section .col-md-6 > div').forEach(div => div.classList.toggle('dark-mode'));
        document.querySelector('#acknowledgments').classList.toggle('dark-mode'); // Toggle dark mode for acknowledgments section
        document.querySelectorAll('#acknowledgments .container').forEach(container => container.classList.toggle('dark-mode')); // Toggle dark mode for containers in acknowledgments section
        document.querySelector('.footer').classList.toggle('dark-mode');
        document.querySelector('.small-round-button').classList.toggle('dark-mode');
    }

    // Acknowledgments Slideshow Function
    document.addEventListener('DOMContentLoaded', function () {
        const containers = document.querySelectorAll('#acknowledgments .container');
        const indicatorsContainer = document.querySelector('#acknowledgments .btn-group');
        let index = 0;

        function showContainer(idx) {
            containers.forEach(container => {
                container.style.display = 'none';
            });

            containers[idx].style.display = 'block';
            updateIndicators(idx);
        }

        function updateIndicators(currentIndex) {
            const indicators = Array.from(indicatorsContainer.children);

            indicators.forEach((indicator, idx) => {
                if (idx === currentIndex) {
                    indicator.classList.add('active');
                } else {
                    indicator.classList.remove('active');
                }
            });
        }

        function goToContainer(idx) {
            index = idx;
            showContainer(index);
        }

        // Create indicators
        containers.forEach((_, idx) => {
            const indicator = document.createElement('div');
            indicator.classList.add('indicator');
            if (idx === 0) {
                indicator.classList.add('active');
            }
            indicator.addEventListener('click', () => goToContainer(idx));
            indicatorsContainer.appendChild(indicator);
        });

        // Automatic slideshow
        function startSlideshow() {
            showContainer(index);
            index = (index + 1) % containers.length;
            setTimeout(startSlideshow, 4000); // 4000 milliseconds = 4 seconds
        }

        // Start the slideshow
        startSlideshow();
    });

    // Fetch visitor count and update it
    async function fetchVisitorCount() {
        try {
            const response = await fetch('https://azureresumeapp.azurewebsites.net/api/getresumedata?id=json&lang=en');
            const data = await response.json();
            document.getElementById('visitorCount').textContent = data.visitorCount;
        } catch (error) {
            console.error('Error fetching visitor count:', error);
            document.getElementById('visitorCount').textContent = 'Error loading count';
        }
    }

    // Increase visitor count
    async function increaseVisitorCount() {
        try {
            await fetch('https://azureresumeapp.azurewebsites.net/api/getresumedata?id=json&lang=en', {
                method: 'POST'
            });
        } catch (error) {
            console.error('Error incrementing visitor count:', error);
        }
    }

    // Call the function to fetch the visitor count and increase the count when the page loads
    document.addEventListener('DOMContentLoaded', () => {
        fetchVisitorCount();
        increaseVisitorCount();
    });
</script>
</body>
</html>
        """
        return func.HttpResponse(
            body=detailed_instructions,
            mimetype="text/html",
            status_code=200
        )

    # Proceed with retrieving resume data if resume_id and lang are provided
    try:
        query = f"SELECT c FROM c WHERE c.id = '{resume_id}' AND c.lang = '{lang}'"
        if filter_by:
            query += f" AND ARRAY_CONTAINS(c.sections, '{{\"type\": \"{filter_by}\"}}')"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))

        if items:
            resume_data = items[0]['c']
            logging.info(f'Resume found: {resume_data}')

            # Remove the specified sections
            keys_to_remove = ['_rid', '_self', '_etag', '_attachments', '_ts', 'id', 'lang', 'sections', 'count']
            for key in keys_to_remove:
                resume_data.pop(key, None)

            # Apply theme filtering
            if theme == 'minimal':
                resume_data = {
                    'basics': resume_data.get('basics', {}),
                    'work': resume_data.get('work', [])
                }
            # Add pagination if requested
            if page and page_size:
                try:
                    page = int(page)
                    page_size = int(page_size)
                    start_index = (page - 1) * page_size
                    end_index = start_index + page_size
                    resume_data = resume_data['work'][start_index:end_index]  # Adjusted for 'work' section
                except ValueError:
                    logging.error('Invalid page or page size')
                    return func.HttpResponse(
                        body=json.dumps({"error": "Invalid page or page size"}),
                        mimetype="application/json",
                        status_code=400
                    )

            # Increment visitor count
            increment_visitor_count()
            visitor_count = get_visitor_count()

            # Add metadata
            timestamp_now = datetime.utcnow().isoformat() + "Z"
            response_message = f"Oyeniyi Emmanuel resume retrieved successfully. Kudos to the organizers (Rishab Kumar and Ifeanyi Otuonye)!"

            response_data = {
                "message": response_message,
                "timestamp": timestamp_now,
                "visitorCount": visitor_count,
                "data": resume_data
            }

            # Return pretty-printed JSON response
            return func.HttpResponse(
                body=json.dumps(response_data, indent=4),
                mimetype="application/json",
                status_code=200
            )
        else:
            logging.error(f'Resume not found - ID: {resume_id}, Lang: {lang}')
            return func.HttpResponse(
                body=json.dumps({"error": "Resume not found"}),
                mimetype="application/json",
                status_code=404
            )
    except exceptions.CosmosResourceNotFoundError:
        logging.error(f'Resume not found - ID: {resume_id}, Lang: {lang}')
        return func.HttpResponse(
            body=json.dumps({"error": "Resume not found"}),
            mimetype="application/json",
            status_code=404
        )
    except Exception as e:
        logging.error(f'Error retrieving resume: {str(e)}')
        return func.HttpResponse(
            body=json.dumps({"error": "Internal server error"}),
            mimetype="application/json",
            status_code=500
        )