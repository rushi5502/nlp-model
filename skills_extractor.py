import fitz  # PyMuPDF
import re
import requests

def extract_text_from_pdf(pdf_url):
    """Extract text from a PDF file from a URL."""
    text = ""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Ensure the request was successful
        pdf_content = response.content

        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        for page in pdf_document:
            text += page.get_text("text")
        pdf_document.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_skills_from_text(text):
    """Extract skills from the text using a comprehensive list of skills."""
    skills = []

    # Comprehensive list of computer science and web development skills
    predefined_skills = [
    'Python', 'JavaScript', 'React', 'Node.js', 'Java', 'C++', 'SQL', 'Django', 'Ruby', 'PHP',
    'HTML', 'CSS', 'Swift', 'Kotlin', 'TypeScript', 'Go', 'Rust', 'MATLAB', 'SAS', 'R',
    'Machine Learning', 'Deep Learning', 'Data Science', 'Hadoop', 'Spark', 'TensorFlow',
    'PyTorch', 'Scikit-Learn', 'NLP', 'Computer Vision', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
    'CI/CD', 'DevOps', 'Git', 'REST', 'GraphQL', 'API Development', 'Unix', 'Linux', 'Windows',
    'Cryptography', 'Blockchain', 'Embedded Systems', 'Cloud Computing', 'Virtualization',
    'Algorithms', 'Data Structures', 'Operating Systems', 'Compilers', 'Network Security', 'Ethical Hacking', 'Penetration Testing',
    'HTML5', 'CSS3', 'JavaScript ES6', 'Bootstrap', 'Sass', 'Less', 'jQuery', 'Angular', 'Vue.js', 'Webpack', 'Gulp', 'Grunt',
    'Responsive Design', 'Node.js', 'Express.js', 'Django', 'Flask', 'Laravel', 'Ruby on Rails', 'ASP.NET', 'Spring Boot', 'Socket.io',
    'WebSockets', 'JWT', 'OAuth', 'GitHub', 'GitLab', 'Bitbucket', 'Cloud Hosting', 'Heroku', 'Netlify', 'Vercel',
    'Google Cloud Platform (GCP)', 'Docker', 'Kubernetes', 'Data Mining', 'Text Mining', 'Image Processing', 'Time Series Analysis', 
    'Reinforcement Learning', 'Transfer Learning', 'Anomaly Detection', 'Feature Engineering', 'Feature Selection', 'Data Wrangling', 
    'Data Cleaning', 'Data Visualization', 'Tableau', 'Power BI', 'QlikView', 'MATPLOTLIB', 'Seaborn', 'Plotly', 'Bokeh', 'ggplot2', 'Dash', 
    'H2O', 'Apache Kafka', 'Apache Storm', 'Data Pipelines', 'ETL', 'Data Warehousing', 'Snowflake', 'Redshift', 'BigQuery', 'Presto', 'Athena', 
    'Apache Airflow', 'Luigi', 'MLflow', 'TensorBoard', 'Natural Language Processing (NLP)', 'OpenCV', 'Keras', 'Chainer', 'CNTK', 'Pandas', 
    'Numpy', 'SciPy', 'Jupyter Notebooks', 'Colab', 'SQLAlchemy', 'NoSQL', 'MongoDB', 'Cassandra', 'HBase', 'Redis', 'CouchDB', 'Elasticsearch', 
    'Graph Databases', 'Neo4j', 'Gremlin', 'SPARQL', 'Scikit-learn', 'XGBoost', 'LightGBM', 'CatBoost', 'Grid Search', 'Random Search', 
    'Bayesian Optimization', 'AutoML', 'TPOT', 'H2O AutoML', 'Auto-sklearn', 'Google AI Platform', 'Amazon SageMaker', 'Azure ML Studio', 
    'IBM Watson', 'Flink', 'MapReduce', 'Pig', 'Hive', 'Standardization', 'Normalization', 'Imputation', 'Feature Extraction', 
    'Dimensionality Reduction', 'PCA', 't-SNE', 'UMAP', 'Bagging', 'Boosting', 'Stacking', 'Blending', 'Recommendation Systems', 
    'Collaborative Filtering', 'Content-Based Filtering', 'Hybrid Systems', 'Graph Algorithms', 'PageRank', 'Community Detection', 
    'Graph Embeddings', 'Social Network Analysis', 'Sentiment Analysis', 'Topic Modeling', 'Latent Dirichlet Allocation (LDA)', 
    'Non-Negative Matrix Factorization (NMF)', 'Image Classification', 'Object Detection', 'Semantic Segmentation', 'Instance Segmentation', 
    'Generative Models', 'Variational Autoencoders (VAEs)', 'Supervised Learning', 'Unsupervised Learning', 'Semi-Supervised Learning', 
    'Self-Supervised Learning', 'Reinforcement Learning', 'Q-Learning', 'Policy Gradient', 'Deep Q-Networks (DQN)', 'Actor-Critic Methods', 
    'Multi-Agent'
]


    # Convert text to lowercase for case-insensitive matching
    lower_text = text.lower()

    # Define a regular expression pattern for exact word matching
    for skill in predefined_skills:
        # Create a pattern that matches whole words only
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, lower_text):
            skills.append(skill)

    # Remove duplicates by converting to a set and back to a list
    return list(set(skills))

def extract_skills_from_resume(resume_url):
    """Extract skills from resume PDF content."""
    text = extract_text_from_pdf(resume_url)
    skills = extract_skills_from_text(text)
    return skills

def match_skills(extracted_skills, required_skills):
    """Match extracted skills with required skills."""
    # Convert both lists to lowercase for case-insensitive comparison
    lower_extracted_skills = [skill.lower() for skill in extracted_skills]
    lower_required_skills = [skill.lower() for skill in required_skills]

    matched_skills = set(lower_extracted_skills).intersection(set(lower_required_skills))
    # Capitalize the first letter for display purposes
    return [skill.capitalize() for skill in matched_skills]

# # Example usage
# resume_url = 'https://utfs.io/f/92daf0c8-fd7a-4984-a391-d076be19e7c7-qc0ivq.pdf'
# required_skills = ["React", "JavaScript", "Python"]

# extracted_skills = extract_skills_from_resume(resume_url)
# print("Extracted Skills:", extracted_skills)

# matched_skills = match_skills(extracted_skills, required_skills)
# print("Matched Skills:", matched_skills)
