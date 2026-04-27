import requests
import json
from typing import Dict, List, Optional
from app.models.review import Review
from app.core.config import settings


class AIReviewService:
    """AI评价审核服务 - 使用DeepSeek API进行智能审核"""
    
    @classmethod
    def analyze_review(cls, review: Review) -> Dict:
        """使用AI分析评价内容，给出审核建议和自动回复"""
        content = review.content
        rating = review.rating
        
        # 构建AI分析请求
        prompt = f"""
请作为专业的社区助餐服务评价审核专家，分析以下用户评价并给出审核建议和自动回复。

评价内容：{content}
评分：{rating}分（5分制）

请按照以下JSON格式返回分析结果：
{{
    "suggestion": "approved"或"rejected"或"pending",
    "confidence": 0.0-1.0之间的置信度,
    "reason": "审核建议的详细理由",
    "keywords": ["关键词1", "关键词2"],
    "risk_level": "low"或"medium"或"high",
    "auto_reply": "针对该评价的自动回复内容（如果不需要回复则返回null）"
}}

审核标准：
1. approved（通过）：评价内容积极正面，符合社区服务规范，没有违规内容
2. rejected（拒绝）：评价包含敏感词、恶意内容、虚假信息或违反社区规定
3. pending（待审核）：内容需要人工进一步判断

自动回复要求：
- 对于积极评价：表达感谢，鼓励继续支持
- 对于中性评价：表达感谢，说明会继续改进
- 对于负面评价：表达歉意，说明会重视并改进
- 回复语言要礼貌、专业、真诚
- 如果评价内容不适合自动回复（如投诉、严重问题），请返回null

请基于评价内容的语义理解进行分析，而不仅仅是关键词匹配。
        """
        
        try:
            # 调用DeepSeek API
            response = cls._call_deepseek_api(prompt)
            
            # 解析AI响应
            if response and response.status_code == 200:
                ai_result = response.json()
                content = ai_result.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                # 尝试解析JSON格式的响应
                try:
                    analysis_result = json.loads(content)
                    return {
                        'review_id': review.id,
                        'suggestion': analysis_result.get('suggestion', 'pending'),
                        'confidence': analysis_result.get('confidence', 0.5),
                        'reason': analysis_result.get('reason', 'AI分析结果'),
                        'keywords': analysis_result.get('keywords', []),
                        'risk_level': analysis_result.get('risk_level', 'medium'),
                        'ai_analyzed': True
                    }
                except json.JSONDecodeError:
                    # 如果JSON解析失败，使用备用逻辑
                    return cls._fallback_analysis(review, content)
            else:
                # API调用失败，使用备用逻辑
                return cls._fallback_analysis(review, f"API调用失败: {response.status_code if response else 'No response'}")
                
        except Exception as e:
            print(f"AI分析错误: {e}")
            return cls._fallback_analysis(review, str(e))
    
    @classmethod
    def batch_analyze_reviews(cls, reviews: List[Review]) -> List[Dict]:
        """批量分析多个评价"""
        results = []
        for review in reviews:
            result = cls.analyze_review(review)
            results.append(result)
        return results
    
    @classmethod
    def _call_deepseek_api(cls, prompt: str) -> Optional[requests.Response]:
        """调用DeepSeek API"""
        url = f"{settings.DEEPSEEK_API_URL}/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": "你是一个专业的社区助餐服务评价审核专家。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            return response
        except requests.RequestException as e:
            print(f"DeepSeek API调用失败: {e}")
            return None
    
    @classmethod
    def _fallback_analysis(cls, review: Review, error_message: str) -> Dict:
        """备用分析逻辑（当AI API调用失败时）"""
        content = review.content.lower()
        rating = review.rating
        
        # 简单的关键词分析作为备用
        sensitive_words = ['投诉', '垃圾', '难吃', '恶心', '脏', '头发', '虫子', '变质']
        positive_words = ['很好', '满意', '好吃', '美味', '感谢', '不错', '好评']
        
        has_sensitive = any(word in content for word in sensitive_words)
        has_positive = any(word in content for word in positive_words)
        
        if has_sensitive:
            return {
                'review_id': review.id,
                'suggestion': 'rejected',
                'confidence': 0.85,
                'reason': f'包含敏感词，建议拒绝（备用逻辑）',
                'keywords': [word for word in sensitive_words if word in content],
                'risk_level': 'high',
                'ai_analyzed': False,
                'error': error_message,
                'auto_reply': None
            }
        elif has_positive or rating >= 4:
            auto_reply = "感谢您的好评！我们会继续努力提供更好的服务，期待您的再次光临。"
            return {
                'review_id': review.id,
                'suggestion': 'approved',
                'confidence': 0.8,
                'reason': '评价内容积极，建议通过（备用逻辑）',
                'keywords': [word for word in positive_words if word in content],
                'risk_level': 'low',
                'ai_analyzed': False,
                'error': error_message,
                'auto_reply': auto_reply
            }
        elif rating == 3:
            auto_reply = "感谢您的评价！我们会认真对待您的反馈，继续改进服务质量。"
            return {
                'review_id': review.id,
                'suggestion': 'approved',
                'confidence': 0.75,
                'reason': '评价内容中性，建议通过（备用逻辑）',
                'keywords': [],
                'risk_level': 'medium',
                'ai_analyzed': False,
                'error': error_message,
                'auto_reply': auto_reply
            }
        else:
            auto_reply = "非常抱歉给您带来不好的体验！我们会重视您的反馈，立即进行改进。如有需要，请联系客服处理。"
            return {
                'review_id': review.id,
                'suggestion': 'pending',
                'confidence': 0.6,
                'reason': '评价内容负面，建议人工审核（备用逻辑）',
                'keywords': [],
                'risk_level': 'medium',
                'ai_analyzed': False,
                'error': error_message,
                'auto_reply': auto_reply
            }
    
    @classmethod
    def get_confidence_level(cls, confidence: float) -> str:
        """根据置信度返回级别"""
        if confidence >= 0.9:
            return 'high'
        elif confidence >= 0.7:
            return 'medium'
        else:
            return 'low'
    
    @classmethod
    def should_auto_approve(cls, analysis_result: Dict) -> bool:
        """判断是否应该自动通过"""
        return analysis_result['confidence'] >= 0.9 and analysis_result['suggestion'] == 'approved'
    
    @classmethod
    def should_auto_reject(cls, analysis_result: Dict) -> bool:
        """判断是否应该自动拒绝"""
        return analysis_result['confidence'] >= 0.85 and analysis_result['suggestion'] == 'rejected'


ai_review_service = AIReviewService()