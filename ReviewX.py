from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CodingalReviewer:
    def __init__(self, number, password, log_callback=None,review_callback = None):
        self.number = number
        self.password = password
        self.log_callback = log_callback
        self.review_callback = review_callback
        
        self.driver = None
        self.wait = None
        self.review_cancel = False
        self.user_data = {}
        self.project_count = None
        
    def update(self, message):
        if self.log_callback:
            self.log_callback(message)
    
    def send_review_tracker_update(self,message):
        if self.review_callback:
            self.review_callback(message)
    
    def store_user_details(self, src, name):
        self.user_data = {"Name": name, "Picture": src}
    
    def get_user_details(self):
        return self.user_data
    
    def get_project_count(self):
        return self.project_count
    
    def cancel(self):
        self.review_cancel = True
    
    def login(self):
        try:
            self.update("🚀 Launching the Codingal universe... Buckle up!")
            self.driver.get("https://www.codingal.com/")
            time.sleep(1)
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
            login_button.click()
            time.sleep(1)
            self.update("Logging in to your dashboard")
            phone_input = self.wait.until(EC.presence_of_element_located((By.NAME, "phone")))
            phone_input.send_keys(self.number)
            time.sleep(0.5)
            login_btn_1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]")))
            login_btn_1.click()
            time.sleep(0.5)
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys(self.password)
            time.sleep(0.25)
            login_btn_2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]")))
            login_btn_2.click()
            time.sleep(0.25)
            profile_pic = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Profile Image']")))
            profile_pic_src = profile_pic.get_attribute("src")
            time.sleep(0.25)
            teacher_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex-col')]/h2")))
            teacher_name = teacher_name_elem.text
            time.sleep(0.25)
            self.store_user_details(profile_pic_src, teacher_name)
            time.sleep(0.25)
            self.update(f"Login successful. Welcome aboard, Captain {teacher_name}!")
        except Exception as e:
            self.update(f"Error During Login: Please Check Your Credentials Again.")
       
    
    def pending_project_count(self):
        self.driver.get("https://www.codingal.com/teacher/dashboard/projects/")
        try:
            time.sleep(0.5)
            project_number_elem = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'font-600') and contains(@class, 'text-lg') and contains(@class, 'text-yellow-200')]"))
            )
            return int(project_number_elem.text)
        except Exception:
            self.update("Hmm... Can't find any projects. Maybe it's time for a coffee?")
            return 0
    
    def generate_review(self, name, lesson):
        try:
            openings = [
                f"Congratulations {name} on completing {lesson}!",
                f"Awesome job on finishing {lesson}, {name}!",
                f"Well done {name} for submitting your {lesson} project!",
                f"{name}, great effort on your {lesson} work!",
                f"You did it, {name}! {lesson} is complete!"
            ]

            compliments = [
                f"{name}, your creativity really shines through in the {lesson} project.",
                f"I can see the effort and thought you've put into {lesson}, {name}.",
                f"{name}, you're developing some solid skills through your work on {lesson}.",
                f"You're getting better with every project, and {lesson} is a great example of that, {name}.",
                f"Your {lesson} submission reflects clear understanding and imagination, {name}.",
                f"{name}, this {lesson} project shows great progress from your previous submissions.",
                f"Impressive attention to detail in your {lesson} project, {name}.",
                f"{name}, your approach to solving challenges in {lesson} is evolving beautifully."
            ]

            encouragements = [
                f"Keep up the amazing work! {name}",
                f"You're on the right path {name} — stay consistent!",
                f"Proud of your progress {name}. Keep going!",
                "Excited to see what you'll do next!",
                f"Keep pushing your limits {name} — you're doing great!",
                "Keep challenging yourself — the sky's the limit!"
            ]

            review_text = (
                f"{random.choice(openings)} "
                f"{random.choice(compliments)} {random.choice(compliments)} "
                f"{random.choice(encouragements)} {random.choice(encouragements)} "
            )
            return review_text
        except Exception:
            return f"Congratulations {name} on completing {lesson}! Your dedication and effort are commendable."


    def review_project(self):
        try:
            self.send_review_tracker_update("Review engine warming up...")
            time.sleep(0.25)
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Review now')])[1]")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            student_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Submitted by')]/preceding-sibling::p")))
            student_name = student_name_elem.text

            self.send_review_tracker_update(f"Scanning {student_name}'s masterpiece...")

            lesson_name_elem = self.driver.find_element(By.XPATH, "//div[@class='flex items-center flex-wrap']/p[contains(@class, 'text-xl') and contains(@class, 'font-600')]")
            lesson_name =  lesson_name_elem .text


            review_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Review now')]")))
            review_btn.click()
            time.sleep(0.5)
            
            textarea = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            review = self.generate_review(student_name, lesson_name)
            textarea.send_keys(review)
            self.send_review_tracker_update(f"Crafting thoughtful feedback for Lesson: {lesson_name}")
            try:
                enhance_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[.//span[text()='Enhance with AI']]")))
                enhance_btn.click()
                time.sleep(3)
            except Exception:
                pass
            self.send_review_tracker_update("Calculating star power")
            stars = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rating-star")))
            given_stars = random.choice([3,4])  # zero-based index; clicks 4th or 5th star
            stars[given_stars].click()
            time.sleep(0.5)
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit review')]")))
            submit_btn.click()
            self.send_review_tracker_update("Review Submitted")
            time.sleep(0.5)
            self.update(f"Feedback sent successfully to {student_name}.")
            back_to_projects = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Back to projects')])")))
            back_to_projects.click()
            time.sleep(1)
        except Exception as e:
            self.update(f"Error during review")

    def start_review(self):
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)...")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        self.login()
        self.review_cancel = False
      
      
        while True:
            pending_projects = self.pending_project_count()
            self.project_count = pending_projects
            
            if pending_projects == 0:
                self.update("Mission accomplished! All projects are reviewed. Time to celebrate")
                break
            
            if self.review_cancel:
                self.update("Review paused. All engines cooling down...")
                break
            
            try:
                self.review_project()
            except Exception as e:
                self.update(f"Error inside start_review, moving forward")
                continue
        
        self.driver.quit()
