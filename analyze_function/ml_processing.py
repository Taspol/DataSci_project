import streamlit as st
import time
import numpy as np
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import numpy as np

def analyze_category(data):
    fig = px.scatter(data, x='PCA1', y='PCA2', color='auto_label', 
                 hover_data={ "dc:title":True},
                 title="Cluster Visualization with Auto-Labeling",
                 labels={'auto_label': 'Research Field'},
                 height=900
                 )

    return fig

def analyze_webscrape(df):
    df['text'] = df['title'] + " " + df['field'] # Repeat the author keywords portion to increase weight
    df['text'] = df['text'].fillna('')


    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english',max_features=1000)
    X = vectorizer.fit_transform(df['text'])

    # Apply KMeans clustering (let's assume we want 5 clusters)
    n_clusters = 10  # Adjust the number of clusters based on your dataset
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    # Define predefined categories with associated keywords (for example purposes)
    category_keywords = {
        'Computer Science': [
            'Artificial Intelligence (AI)', 'Machine Learning (ML)', 'Deep Learning', 
            'Neural Networks', 'Natural Language Processing (NLP)', 'Computer Vision', 
            'Robotics', 'Data Science', 'Big Data', 'Data Mining', 'Cloud Computing', 
            'Cybersecurity', 'Blockchain Technology', 'Software Engineering', 
            'Human-Computer Interaction (HCI)', 'Quantum Computing', 'Internet of Things (IoT)', 
            'Augmented Reality (AR)', 'Virtual Reality (VR)', 'Edge Computing', 
            'Distributed Systems', 'Algorithm Design', 'Software Development', 'Predictive Analytics'
        ],
        'Engineering': [
            'Mechanical Engineering', 'Civil Engineering', 'Electrical Engineering', 
            'Aerospace Engineering', 'Nanotechnology', 'Biomedical Engineering', 
            'Environmental Engineering', 'Chemical Engineering', 'Industrial Engineering', 
            'Geotechnical Engineering', 'Structural Engineering', 'Energy Systems', 
            'Automotive Engineering', 'Robotics Engineering', 'Control Systems', 
            'Thermodynamics', 'Fluid Mechanics', 'Vibration Analysis', 'Materials Engineering', 
            'Manufacturing Systems', 'Sustainable Engineering', 'Smart Infrastructure', 
            'Additive Manufacturing (3D Printing)', 'Mechatronics', 'Power Systems'
        ],
        'Biology': [
            'Genetics', 'Molecular Biology', 'Ecology', 'Neuroscience', 'Immunology', 
            'Cell Biology', 'Microbiology', 'Biotechnology', 'Evolutionary Biology', 
            'Pharmacology', 'Biochemistry', 'Biophysics', 'Physiology', 'Endocrinology', 
            'Bioinformatics', 'Marine Biology', 'Plant Biology', 'Genomics', 'Proteomics', 
            'Stem Cell Research', 'Human Biology', 'Synthetic Biology', 'Zoology', 
            'Agricultural Biology', 'Microbial Pathogenesis', 'Human Disease Research'
        ],
        'Health': [
            'Medicine', 'Public Health', 'Nursing', 'Epidemiology', 'Healthcare Management', 
            'Health Policy', 'Medical Research', 'Pharmacology', 'Toxicology', 'Health Economics', 
            'Mental Health', 'Global Health', 'Maternal and Child Health', 'Infectious Diseases', 
            'Chronic Disease Management', 'Health Informatics', 'Biomedical Engineering', 
            'Telemedicine', 'Nutritional Science', 'Healthcare Technology', 
            'Clinical Trials', 'Medical Imaging', 'Genetic Counseling', 'Patient Care'
        ],
        'Physics': [
            'Physics', 'Quantum Mechanics', 'Astrophysics', 'Material Science', 
            'Condensed Matter Physics', 'Particle Physics', 'Theoretical Physics', 
            'Experimental Physics', 'Optics', 'Laser Physics', 'Nuclear Physics', 
            'Plasma Physics', 'High-Energy Physics', 'Quantum Field Theory', 
            'Solid State Physics', 'Statistical Mechanics', 'Gravitational Physics', 
            'String Theory', 'Fluid Dynamics', 'Nonlinear Dynamics', 'Cosmology', 
            'Astroparticle Physics', 'Geophysics', 'Radio Frequency (RF) Physics', 
            'Semiconductor Physics', 'Thermal Physics', 'Electromagnetism'
        ]
    }


    # Function to label a cluster based on the most common words in that cluster
    def label_cluster(cluster_center, category_keywords):
        # Find the closest category based on common keywords
        min_distance = float('inf')
        closest_category = None
        
        for category, keywords in category_keywords.items():
            # Calculate the distance between the cluster center and the keywords of each category
            category_vec = vectorizer.transform([' '.join(keywords)])
            dist = np.linalg.norm(cluster_center - category_vec.mean(axis=0))
            
            if dist < min_distance:
                min_distance = dist
                closest_category = category
        
        return closest_category

    # Assign a label to each cluster based on the category keywords
    cluster_centers = kmeans.cluster_centers_
    cluster_labels = []

    for center in cluster_centers:
        label = label_cluster(center, category_keywords)
        cluster_labels.append(label)

    # Add the auto-label to the dataframe
    df['auto_label'] = df['cluster'].apply(lambda x: cluster_labels[x])

    # Use PCA to reduce the dimensionality of the data to 2D for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X.toarray())

    # Add PCA components to the dataframe
    df['PCA1'] = pca_result[:, 0]
    df['PCA2'] = pca_result[:, 1]

    # Plot the clusters using Plotly, with HTML line breaks in the hover data
    fig = px.scatter(df, x='PCA1', y='PCA2', color='auto_label', 
                    hover_data={'title': True},
                    title="Cluster Visualization with Auto-Labeling",
                    labels={'auto_label': 'Research Field'})
    # fig.show(renderer="browser")
    # fig.show(renderer="browser")
    return fig

    