from app.models import User, Daily, Repository, Task, Todo
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app.models import db


def register_db_utils(app: Flask) -> None:
    """Database testing utilities."""

    @app.cli.command("db-fake")
    def db_fake_data() -> None:
        """Commit dummy data to the database."""
        with app.app_context():
            # Create Users
            user_a = User.add("Patryk@email.com", "Patryk", "Patryk12345")
            user_b = User.add("Filip@email.com", "Filip", "Filip12345")
            user_c = User.add("Paweł@email.com", "Paweł", "Paweł12345")
            user_d = User.add("Natalia@email.com", "Natalia", "Natalia12345")
            user_e = User.add("Ela@email.com", "Ela", "Ela12345")
            user_f = User.add("Michał@email.com", "Michał", "Michał12345")
            user_g = User.add("Pawlo@email.com", "Pawlo", "Pawlo12345")
            user_h = User.add("Maciej@email.com", "Maciej", "Maciej12345")
            user_i = User.add("Mateusz@email.com", "Mateusz", "Mateusz12345")
            user_j = User.add("Ola@email.com", "Ola", "Ola12345")
            user_k = User.add("Krzysztof@email.com", "Krzysztof", "Krzysztof2345")
            user_l = User.add("Kamil@email.com", "Kamil", "Kamil12345")
            user_m = User.add("Karol@email.com", "Karol", "Karol12345")
            user_n = User.add("Piotr@email.com", "Piotr", "Piotr12345")
            user_o = User.add("Piotrek@email.com", "Piotrek", "Piotrek12345")
            user_p = User.add("Agata@email.com", "Agata", "Agata12345")
            user_r = User.add("Diego@email.com", "Diego", "Diego12345")
            user_s = User.add("Bartek@email.com", "Bartek", "Bartek12345")
            user_t = User.add("Łukasz@email.com", "Łukasz", "Łukasz12345")
            user_u = User.add("Wojtek@email.com", "Wojtek", "Wojtek12345")
            user_w = User.add("Wojciech@email.com", "Wojciech", "Wojciech12345")
            

            # Create daily for all users
            for i in range(20):
                Daily.add("Wake up and make the bed", str(i))
                Daily.add("Brush teeth and take a shower or bath", str(i))
                Daily.add("Make breakfast and eat", str(i))
                Daily.add("Attend meetings or classes", str(i))
                Daily.add("Take breaks and eat lunch", str(i))
                Daily.add("Continue work or classes", str(i))
                Daily.add("Exercise or engage in physical activity", str(i))
                Daily.add("Prepare dinner and eat", str(i))
                Daily.add("Spend time with family or friends", str(i))
                Daily.add("Read or engage in a hobby", str(i))
                Daily.add("Review and plan for the next day", str(i))
                Daily.add("Brush teeth and get ready for bed", str(i))
                Daily.add("Turn off electronics and read a book or meditate before sleep", str(i))
                Daily.add("Go to bed at a reasonable hour", str(i))

            # Create Repositories
            repo1 = Repository.add(
                "PixelPerfect",
                "A repository containing code for image processing and editing tools.",
                user_a,
            )
            repo2 = Repository.add(
                "EcoSystem",
                "A repository containing code and resources for studying and simulating natural ecosystems.",
                user_u,
            )
            repo3 = Repository.add(
                "SmartHome",
                "A repository containing code and resources for building and controlling smart home devices.",
                user_w,
            )
            Repository.add(
                "FitnessTracker",
                "A repository containing code and resources for creating fitness tracking and monitoring apps.",
                user_b,
            )
            Repository.add(
                "DataVault",
                "A repository containing code and resources for securely storing and managing large amounts of data.",
                user_c,
            )
            Repository.add(
                "CodeNinja",
                "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                user_d,
            )
            Repository.add(
                "AI_Assistant",
                "A repository containing code snippets, tutorials, and resources for learning programming and software development.",
                user_e,
            )
            Repository.add(
                "BlockchainBasics",
                "A repository containing code and resources for learning about blockchain technology.",
                user_f,
            )
            Repository.add(
                "WebCrawler",
                "A repository containing code for building web crawlers and scraping data from websites.",
                user_g,
            )
            Repository.add(
                "CloudComputing",
                "A repository containing code and resources for building and managing cloud computing systems.",
                user_h,
            )
            Repository.add(
                "VirtualReality",
                "A repository containing code and resources for creating virtual reality experiences.",
                user_i,
            )
            Repository.add(
                "SecurePasswords",
                "A repository containing code and resources for implementing secure password storage and management.",
                user_j,
            )
            Repository.add(
                "MachineLearning",
                "A repository containing pre-trained machine learning models and resources for training and deploying new models.",
                user_k,
            )
            Repository.add(
                "ImageRecognition",
                "A repository containing code and resources for implementing image recognition algorithms.",
                user_l,
            )
            Repository.add(
                "CypherCode",
                "A repository containing code and resources for encrypting and decrypting messages and data.",
                user_m,
            )
            Repository.add(
                "RealTimeAnalytics",
                "A repository containing code and resources for processing and analyzing data in real-time.",
                user_n,
            )
            Repository.add(
                "QuantumComputing",
                "A repository containing code and resources for learning about quantum computing and building quantum algorithms.",
                user_p,
            )
            Repository.add(
                "DeepLearning",
                "A repository containing code and resources for implementing deep learning algorithms",
                user_a,
            )        
            Repository.add(
                "NeuralNetworks",
                "A repository containing code and resources for building and training neural networks",
                user_a,
            )    
            Repository.add(
                "DistributedSystems",
                " A repository containing code and resources for building and managing distributed systems.",
                user_a,
            )

            repo1.participants.append(user_b)
            repo1.participants.append(user_c)
            repo1.participants.append(user_d)
            repo1.participants.append(user_e)
            repo1.participants.append(user_f)
            repo1.participants.append(user_g)
            repo2.participants.append(user_a)
            repo3.participants.append(user_a)
            
            task_a = Task.add(
                "Website Design",
                "A task that involves creating a document outlining the goals, objectives, and methods for a proposed project or initiative.",
                repo1.contents[0].id,
            )
            task_b = Task.add(
                "Project Proposal",
                "A task that involves creating a visually appealing and user-friendly website that meets the needs of the client or business.",
                repo1.contents[1].id,
            )
            task_c = Task.add(
                "Data Analysis",
                "A task that involves collecting, cleaning, and analyzing data to make informed decisions or draw conclusions.",
                repo1.contents[2].id,
            )
            task_d = Task.add(
                "Data Analysis",
                "A task that involves collecting, cleaning, and analyzing data to make informed decisions or draw conclusions.",
                repo1.contents[0].id,
            )
            task_e = Task.add(
                "Marketing Campaign",
                "A task that involves planning and executing a marketing campaign to promote a product or service.",
                repo1.contents[0].id,
            )
            task_f = Task.add(
                "Software Development",
                "A task that involves designing, coding, and testing software to meet specific requirements.",
                repo1.contents[0].id,
            )
            task_g = Task.add(
                "Financial Forecasting",
                "A task that involves analyzing past financial data and making predictions about future financial performance.",
                repo1.contents[1].id,
            )
            task_h = Task.add(
                "Content Creation",
                "A task that involves writing, designing, or producing content such as articles, videos, or graphics.",
                repo1.contents[1].id,
            )
            task_i = Task.add(
                "IT Support",
                "A task that involves providing technical assistance and troubleshooting for computer systems and networks.",
                repo1.contents[0].id,
            )
            task_j = Task.add(
                "Social Media Management",
                "A task that involves creating, scheduling and publishing content on social media platforms, monitoring and responding to comments and direct messages, and analyzing metrics.",
                repo1.contents[2].id,
            )
            task_k = Task.add(
                "Customer Service",
                " A task that involves interacting with customers to provide information, solve problems, and ensure customer satisfaction.",
                repo1.contents[2].id,
            )  

            Todo.add("Gather information about the client's needs and preferences", task_a.id)
            Todo.add("Create wireframes or mockups of the website", task_a.id)
            Todo.add("Design the website layout and graphics", task_a.id)
            Todo.add("Develop the website using HTML, CSS, and JavaScript", task_a.id,)
            Todo.add("Test and optimize the website for different devices and browsers", task_a.id,)
            
            Todo.add("Research and gather information about the proposed project", task_b.id)
            Todo.add("Create an outline for the proposal document", task_b.id)
            Todo.add("Write the proposal document", task_b.id)
            Todo.add("Review and edit the proposal document", task_b.id,)
            Todo.add("Submit the proposal document", task_b.id,)
            
            Todo.add("Collect and organize data from various sources", task_c.id)
            Todo.add("Clean and prepare the data for analysis", task_c.id)
            Todo.add("Perform statistical analyses or use machine learning algorithms", task_c.id)
            Todo.add("Create visualizations to display the results", task_c.id,)
            Todo.add("Write a report or present the findings to stakeholders", task_c.id,)
            
            Todo.add("Define the target audience and goals of the campaign", task_d.id)
            Todo.add("Research and select appropriate marketing channels", task_d.id)
            Todo.add("Develop the content and materials for the campaign", task_d.id)
            Todo.add("Execute the campaign and track its progress", task_d.id,)
            Todo.add("Analyze and evaluate the campaign's effectiveness", task_d.id,)
            
            Todo.add("Understand and analyze the requirements of the software", task_e.id)
            Todo.add("Design and plan the architecture of the software", task_e.id)
            Todo.add("Write the code and test it on different platforms", task_e.id)
            Todo.add("Debug and troubleshoot any issues that arise", task_e.id,)
            Todo.add("Deploy the software and provide maintenance", task_e.id,)
            
            Todo.add("Gather financial data from previous years", task_f.id)
            Todo.add("Analyze the historical data to identify trends and patterns", task_f.id)
            Todo.add("Create a financial model to make predictions", task_f.id)
            Todo.add("Use various forecasting methods to generate different scenarios", task_f.id,)
            Todo.add("Present the findings and provide recommendations", task_f.id,)
            
            Todo.add("Research the topic and gather information", task_g.id)
            Todo.add("Create an outline for the content", task_g.id)
            Todo.add("Write the content and revise it", task_g.id)
            Todo.add("Add images, videos, or other media to enhance the content", task_g.id,)
            Todo.add("Publish the content and promote it", task_g.id,)
            
            Todo.add("Plan and schedule the content for the week or month", task_h.id)
            Todo.add("Create and curate engaging content", task_h.id)
            Todo.add("Monitor and respond to comments and direct messages", task_h.id)
            Todo.add("Analyze metrics and adjust the strategy accordingly", task_h.id,)
            Todo.add("Collaborate with other departments or agencies", task_h.id,)
            
            Todo.add("Respond to customer inquiries via phone, email, or chat", task_i.id)
            Todo.add("Troubleshoot and solve customer problems", task_i.id)
            Todo.add("Provide information about products or services", task_i.id)
            Todo.add("Follow up with customers to ensure satisfaction", task_i.id,)
            Todo.add("Document customer interactions and provide feedback to improve service.", task_i.id,)
            
            Todo.add("Gather information about the client's needs and preferences", task_j.id)
            Todo.add("Create wireframes or mockups of the website", task_j.id)
            Todo.add("Design the website layout and graphics", task_j.id)
            Todo.add("Develop the website using HTML, CSS, and JavaScript", task_j.id,)
            Todo.add("Test and optimize the website for different devices and browsers", task_j.id,)
            

            db.session.commit()

            print("Success")

    @app.cli.command("db-drop")
    def db_drop_data() -> None:
        """Drop and recreate the database."""
        with app.app_context():
            db.drop_all()
            db.create_all()

    @app.cli.command("db-test")
    def db_test() -> None:
        """Temporary method to test ORM during development."""
