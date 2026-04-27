from typing import Dict, Optional
import os
import json
import requests
from app.models.review import Review
from app.core.config import settings

class AIReplyService:
    """AI回复服务"""
    
    @classmethod
    def generate_reply(cls, review: Review) -> Dict:
        """使用AI生成评价回复"""
        content = review.content
        rating = review.rating
        
        # 根据评价类型（配送员评价或餐品评价）生成不同的回复
        is_deliverer_review = review.deliverer_id is not None
        
        if is_deliverer_review:
            # 配送员评价的回复提示词
            prompt = f"""
请作为专业的社区助餐服务客服人员，根据以下用户对配送服务的评价生成个性化的回复。

用户评价内容：{content}
评分：{rating}分（5分制）

回复要求：
1. 语言要礼貌、专业、真诚，富有情感
2. 针对不同评分有不同的回复策略：
   - 5分（优秀）：热情表达感谢，具体赞美配送服务的优点，使用生动的语言，加入适当的表情符号
   - 4分（良好）：真诚表达感谢，肯定配送服务的优点，同时表达继续提升的决心
   - 3分（一般）：感谢用户的反馈，认真分析问题，表达改进的决心和具体措施
   - 2分（较差）：诚恳道歉，详细说明会如何改进配送服务，提供解决方案
   - 1分（很差）：非常诚恳地道歉，承诺立即调查处理，提供具体的改进措施和联系方式
3. 回复内容要自然活泼，避免生硬的模板化语言，使用多样化的表达方式
4. 可以适当加入表情符号，但不要过多，保持专业形象
5. 回复长度控制在60-120字之间，内容要丰富充实
6. 重点关注配送速度、服务态度、配送人员专业性、配送包装等方面
7. 根据用户评价内容，针对性地回应具体问题，不要泛泛而谈

请直接返回回复内容，不要包含任何其他说明文字。
            """
        else:
            # 餐品评价的回复提示词
            prompt = f"""
请作为专业的社区助餐服务客服人员，根据以下用户对餐品的评价生成个性化的回复。

用户评价内容：{content}
评分：{rating}分（5分制）

回复要求：
1. 语言要礼貌、专业、真诚，富有情感
2. 针对不同评分有不同的回复策略：
   - 5分（优秀）：热情表达感谢，具体赞美餐品的优点，使用生动的语言，加入适当的表情符号
   - 4分（良好）：真诚表达感谢，肯定餐品的优点，同时表达继续提升的决心
   - 3分（一般）：感谢用户的反馈，认真分析问题，表达改进的决心和具体措施
   - 2分（较差）：诚恳道歉，详细说明会如何改进餐品质量，提供解决方案
   - 1分（很差）：非常诚恳地道歉，承诺立即调查处理，提供具体的改进措施和联系方式
3. 回复内容要自然活泼，避免生硬的模板化语言，使用多样化的表达方式
4. 可以适当加入表情符号，但不要过多，保持专业形象
5. 回复长度控制在60-120字之间，内容要丰富充实
6. 重点关注餐品味道、营养搭配、分量、新鲜度、食材质量等方面
7. 根据用户评价内容，针对性地回应具体问题，不要泛泛而谈

请直接返回回复内容，不要包含任何其他说明文字。
            """
        
        try:
            # 调用DeepSeek API
            api_key = settings.DEEPSEEK_API_KEY
            api_url = f"{settings.DEEPSEEK_API_URL}/v1/chat/completions"
            
            # 检查API密钥是否配置
            if not api_key:
                print(f"AI回复失败：API密钥未配置")
                return cls._fallback_reply(review, "API密钥未配置")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": settings.DEEPSEEK_MODEL,
                "messages": [
                    {"role": "system", "content": "你是专业的社区助餐服务客服人员，擅长根据用户评价生成恰当的回复。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            print(f"开始调用AI API...")
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            print(f"API响应状态码: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            reply_content = result["choices"][0]["message"]["content"].strip()
            
            # 移除可能导致编码问题的字符
            import re
            # 移除表情符号和特殊字符
            reply_content = re.sub(r'[\U00010000-\U0010ffff]', '', reply_content)
            
            print(f"AI回复生成成功")
            return {
                "review_id": review.id,
                "reply": reply_content,
                "ai_generated": True,
                "confidence": 0.95,
                "error": None
            }
            
        except Exception as e:
            # 备用回复逻辑
            print(f"AI回复失败：{str(e)}")
            return cls._fallback_reply(review, str(e))
    
    @classmethod
    def _fallback_reply(cls, review: Review, error_message: str) -> Dict:
        """备用回复逻辑（当AI API调用失败时）"""
        rating = review.rating
        
        if rating == 5:
            reply = "感谢您的五星好评！您的满意是我们最大的动力，我们会继续努力提供更好的服务，期待您的再次光临！"
        elif rating == 4:
            reply = "感谢您的好评！我们会继续保持优质服务，不断改进，为您提供更好的用餐体验！"
        elif rating == 3:
            reply = "感谢您的评价！我们会认真对待您的反馈，继续改进服务质量，争取做得更好！"
        elif rating == 2:
            reply = "非常抱歉给您带来不好的体验！我们会重视您的反馈，立即进行改进。如有需要，请联系客服处理。"
        else:
            reply = "非常抱歉给您带来极差的体验！我们会立即调查处理，给您一个满意的答复。请联系客服说明具体情况。"
        
        return {
            "review_id": review.id,
            "reply": reply,
            "ai_generated": False,
            "confidence": 0.8,
            "error": error_message
        }
    
    @classmethod
    def batch_generate_replies(cls, reviews: list[Review]) -> Dict:
        """批量生成回复"""
        results = []
        generated_count = 0
        
        for review in reviews:
            if not review.reply:  # 只处理没有回复的评价
                result = cls.generate_reply(review)
                results.append(result)
                generated_count += 1
        
        return {
            "total_reviews": len(reviews),
            "generated_replies": generated_count,
            "results": results
        }