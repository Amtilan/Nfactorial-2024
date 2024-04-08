
# import google.generativeai as genai


# GOOGLE_API_KEY = "AIzaSyCPzEJyZAJ2QsIZ-FPBLPKJiVJg2bX77dg"
# genai.configure(api_key=GOOGLE_API_KEY)

# generation_config = {
#   "temperature": 0.5,
#   "top_p": 1,
#   "top_k": 1,
#   "max_output_tokens": 2048,
# }

# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT",
#     "threshold": "HIGH"
#   },
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH",
#     "threshold": "HIGH"
#   },
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#     "threshold": "HIGH"
#   },
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#     "threshold": "HIGH"
#   },
# ]

# model = genai.GenerativeModel(model_name="gemini-1.0-pro",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)

# def get_ai(full_text):
#     response = f"Твоя задача заключается в том чтобы полностью обьяснит всю важную информацию в новостной статье очень кратко и ясно.  {full_text}"
#     text1 = model.generate_content(response)
#     # print(text1.text)
#     return text1.text