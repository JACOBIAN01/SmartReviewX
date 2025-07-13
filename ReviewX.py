from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

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
        import traceback
        try:
            self.update("🚀 Opening Codingal Website...")
            self.driver.get("https://www.codingal.com/")
            self.update(f"🌐 Page loaded: {self.driver.title}")
            time.sleep(1.5)

        # Step 1: Find and click Login button
            self.update("🔍 Looking for Login button...")
            try:
                login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
                )
                login_button.click()
                self.update("✅ Login button clicked.")
            except Exception:
                self.update("❌ Login button not found. Possibly UI changed or blocked.")
                return

            time.sleep(1)

            # Step 2: Enter Phone Number
            self.update("📱 Entering Phone Number...")
            phone_input = self.wait.until(EC.presence_of_element_located((By.NAME, "phone")))
            phone_input.clear()
            phone_input.send_keys(self.number)
            time.sleep(0.5)

            # Step 3: Click "Login with password"
            self.update("🔐 Clicking 'Login with password'...")
            login_with_pass = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]"))
                )
            login_with_pass.click()
            time.sleep(0.5)

            # Step 4: Enter password
            self.update("🔑 Entering password...")
            password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(0.5)

            # Step 5: Final login click
            self.update("➡️ Submitting login form...")
            final_login_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]"))
                )
            final_login_btn.click()
            time.sleep(1.5)

        # Step 6: Wait for Dashboard (Profile)
            self.update("🧠 Waiting for dashboard/profile to load...")
            profile_pic = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Profile Image']")))
            profile_pic_src = profile_pic.get_attribute("src")

            teacher_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex-col')]/h2")))
            teacher_name = teacher_name_elem.text

            self.store_user_details(profile_pic_src, teacher_name)
            self.update(f"✅ Login Successful! Hello {teacher_name}")

        except Exception as e:
            error_msg = traceback.format_exc()
            self.update(f"❌ Login Failed: {str(e)}\n{error_msg}")
            self.update("⚠️ Please Cancel & Try Again!")

    
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
            self.send_review_tracker_update("Review Started")
            time.sleep(0.25)
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Review now')])[1]")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            student_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Submitted by')]/preceding-sibling::p")))
            student_name = student_name_elem.text

            self.send_review_tracker_update(f"Analyzing Project for {student_name}")
            
            lesson_name_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Lesson')]")))
            lesson_name = lesson_name_elem.text
            
            review_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Review now')]")))
            review_btn.click()
            time.sleep(0.5)
            
            textarea = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            review = self.generate_review(student_name, lesson_name)
            textarea.send_keys(review)
            self.send_review_tracker_update(f"Generating Review for {lesson_name}")
            try:
                enhance_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[.//span[text()='Enhance with AI']]")))
                enhance_btn.click()
                time.sleep(3)
            except Exception:
                pass
            self.send_review_tracker_update("Analyzing Rating")
            stars = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rating-star")))
            given_stars = random.choice([3,4])  # zero-based index; clicks 4th or 5th star
            stars[given_stars].click()
            time.sleep(0.5)
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit review')]")))
            submit_btn.click()
            self.send_review_tracker_update("Review Submitted")
            time.sleep(0.5)
            self.update(f"Review completed successfully for {student_name}.")
            back_to_projects = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Back to projects')])")))
            back_to_projects.click()
            time.sleep(1)
        except Exception as e:
            self.update(f"Error during review")

    def start_review(self):

        # === Step 2: Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            self.driver = webdriver.Chrome( options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.update("✅Chrome started successfully.")
        except Exception as e:
            self.update(f"❌ Failed to start Chrome: {str(e)}")
            return
        
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
            except Exception as e:
                self.update(f"Error inside start_review, moving forward")
                continue
        
        self.driver.quit()
