from google.cloud import translate

def translate_text_with_model(
    text: str,
    project_id: str,
    model_id: str,
) -> translate.TranslationServiceClient:

    client = translate.TranslationServiceClient()

    location = "eu-east1"
    parent = f"projects/{project_id}/locations/{location}"
    model_path = f"{parent}/models/{model_id}"

    response = client.translate_text(
        request={
            "contents": [text],
            "target_language_code": "uk",
            "model": model_path,
            "source_language_code": "ja",
            "parent": parent,
            "mime_type": "text/plain",
        }
    )

    for translation in response.translations:
        print(f"Translated text: {translation.translated_text}")

    return response

