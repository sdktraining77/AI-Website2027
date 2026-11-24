from transformers import pipeline

nli_model = pipeline("text-classification",model="cross-encoder/nli-deberta-v3-base")


def check_evidence(premise, hypothesis):#premise: النص المسترجع من قاعدة البيانات hypothesis: المعلومة اللي بدنا نتحقق منها.
    result = nli_model({"text": premise, "text_pair": hypothesis})
    # توحيد شكل النتيجة سواء رجعت List أو Dictionary
    if isinstance(result, list):
        result = result[0]

    if not isinstance(result, dict) or "label" not in result or "score" not in result:
        raise ValueError("Unexpected NLI output format: ",result)
    return result
#هاد الموديل وظيفته يفهم العلاقه بين ابنص المسترجع والمعلومه اللي بدي اتاكد انها موجوده بالنص 


"""
Entailment	المعلومة مدعومة
Contradiction	المعلومة متناقضة
Neutral	لا يوجد دليل كافٍ
"""