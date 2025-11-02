import os
import google.generativeai as genai
from typing import Optional
import json

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

def generate_reflection_feedback(
    reflection_content: str,
    framework: Optional[str] = None,
    structure: Optional[str] = None
) -> str:
    """
    Generate AI-powered feedback for student reflection submissions using Google Gemini.
    
    Args:
        reflection_content: The student's reflection text (may be JSON structured)
        framework: The reflection framework being used (e.g., "Bloom's Taxonomy", "5 WHYs", "1-H")
        structure: The custom structure as JSON string containing field labels
    
    Returns:
        AI-generated feedback text
    """
    try:
        # Parse reflection content if it's structured
        reflection_text = ""
        try:
            content_data = json.loads(reflection_content)
            if isinstance(content_data, list) and len(content_data) > 0 and 'label' in content_data[0]:
                # Structured format: convert to readable text
                reflection_text = "\n\n".join([
                    f"{item['label']}:\n{item['response']}"
                    for item in content_data
                ])
            else:
                reflection_text = reflection_content
        except (json.JSONDecodeError, TypeError):
            # Plain text format
            reflection_text = reflection_content
        
        # Build context-aware prompt
        prompt = f"""You are an Educational reflection feedback expert analyzing a student's reflection journal entry. You need to evaluate the feedback based on the configuration framework chosen by the educator."""
        
        if framework:
            prompt += f" The framework chosen by the educator is '{framework}'."
        
        prompt += f"""\n\nYou have to provide feedback separately for each question/label of the reflection. Also, provide constructive, encouraging, specific feedback that can help the student improve and deepen their learning.

Student's Reflection:
{reflection_text}

Please provide your feedback addressing each question/label separately, highlighting what the student did well and suggesting areas for improvement and deeper exploration."""

        # Call Gemini API
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Thank you for your thoughtful reflection. Keep up the great work!"
            
    except Exception as e:
        print(f"Error generating AI feedback: {str(e)}")
        # Fallback to generic positive feedback
        return "Great reflection! Consider elaborating more on your learning outcomes and connecting your insights to real-world applications."
