import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# إعداد عنوان الصفحة
st.set_page_config(page_title="مستخرج النصوص الذكي", page_icon="📝")

st.title("📝 مستخرج النصوص من الصور")
st.write("قم برفع صورة تحتوي على نص باللغة العربية أو الإنجليزية لاستخراجه فوراً.")

# تحميل قارئ النصوص (يدعم العربية والإنجليزية)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['ar', 'en'])

reader = load_reader()

# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # عرض الصورة المرفوعة
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة التي تم رفعها', use_column_width=True)
    
    st.write("---")
    
    with st.spinner('جاري معالجة الصورة واستخراج النص...'):
        # تحويل الصورة إلى تنسيق يفهمه EasyOCR
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0) # detail=0 يعيد النص فقط
        
        if results:
            st.subheader("النص المستخرج:")
            # دمج النصوص المستخرجة في نص واحد
            full_text = "\n".join(results)
            st.text_area(label="", value=full_text, height=300)
            
            # زر لتحميل النص كملف
            st.download_button(label="تحميل النص كملف txt", data=full_text, file_name="extracted_text.txt")
        else:
            st.warning("لم يتم العثور على نص في هذه الصورة.")
