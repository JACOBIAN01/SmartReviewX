from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

class CodingalReviewer:
    def __init__(self, number, password, log_callback=None):
        self.number = number
        self.password = password
        self.log_callback = log_callback
        
        self.driver = None
        self.wait = None
        self.review_cancel = False
        self.user_data = {}
        self.project_count = None
        
    def update(self, message):
        print(message)
        if self.log_callback:
            self.log_callback(message)
    
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
            self.update("Opening Your Dashboard")
            self.driver.get("https://www.codingal.com/")
            time.sleep(1)
            
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
            login_button.click()
            time.sleep(0.5)
            
            phone_input = self.wait.until(EC.presence_of_element_located((By.NAME, "phone")))
            phone_input.send_keys(self.number)
            time.sleep(0.5)
            
            login_btn_1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]")))
            login_btn_1.click()
            time.sleep(0.5)
            
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys(self.password)
            time.sleep(0.5)
            
            login_btn_2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]")))
            login_btn_2.click()
            time.sleep(1)
            
            profile_pic = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Profile Image']")))
            time.sleep(1)
            
            teacher_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex-col')]/h2")))
            teacher_name = teacher_name_elem.text
            time.sleep(1)
            
            profile_pic_src = profile_pic.get_attribute("src")
            time.sleep(1)
            
            self.store_user_details(profile_pic_src, teacher_name)
            time.sleep(1)
            
            self.update(f"Login Successful! Hello {teacher_name}")
        except Exception as e:
            self.update(f"Error During Login: Please Check Your Credentials Again.")
            self.update("Please Cancel & Try Again!")
    
    def pending_project_count(self):
        self.driver.get("https://www.codingal.com/teacher/dashboard/projects/")
        try:
            time.sleep(0.5)
            project_number_elem = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'font-600') and contains(@class, 'text-lg') and contains(@class, 'text-yellow-200')]"))
            )
            return int(project_number_elem.text)
        except Exception:
            self.update("Could not find project count, assuming 0")
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
            time.sleep(1.5)
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Review now')])[1]")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", element)
            
            student_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Submitted by')]/preceding-sibling::p")))
            student_name = student_name_elem.text
            
            lesson_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Lesson')]")))
            lesson_name = lesson_name_elem.text
            
            review_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Review now')]")))
            review_btn.click()
            
            textarea = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            review = self.generate_review(student_name, lesson_name)
            textarea.send_keys(review)
            
            try:
                enhance_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[.//span[text()='Enhance with AI']]")))
                enhance_btn.click()
                time.sleep(3)
            except Exception:
                pass
            
            stars = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rating-star")))
            given_stars = random.choice([3,4])  # zero-based index; clicks 4th or 5th star
            stars[given_stars].click()
            
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit review')]")))
            submit_btn.click()
            
            self.update(f"Review completed successfully for {student_name}.")
            time.sleep(1)
            
            back_to_projects = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Back to projects')])")))
            back_to_projects.click()
            time.sleep(1)
        except Exception as e:
            self.update(f"Error during review")

    def start_review(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        self.login()
        self.review_cancel = False
        
        while True:
            pending_projects = self.pending_project_count()
            self.project_count = pending_projects
            
            if pending_projects == 0:
                self.update("All projects review completed.")
                break
            
            if self.review_cancel:
                self.update("Review cancelled.")
                break
            
            try:
                self.review_project()
                time.sleep(3)
            except Exception as e:
                self.update(f"Error inside start_review, moving forward")
                continue
        
        self.driver.quit()
