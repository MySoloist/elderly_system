from typing import Dict, List, Any
from collections import Counter, defaultdict
import re
import os
import httpx
import json
from datetime import datetime, timedelta

class AIAnalysisService:
    """AI智能分析服务 - 使用DeepSeek API进行真正的智能分析"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    async def analyze_reviews(self, reviews: List[Dict]) -> Dict[str, Any]:
        """
        使用AI模型分析评价数据，生成分析报告
        
        Args:
            reviews: 评价列表
            
        Returns:
            分析报告数据
        """
        if not reviews:
            return {
                "summary": {
                    "total_reviews": 0,
                    "average_rating": 0,
                    "positive_rate": 0,
                    "negative_rate": 0
                },
                "trends": [],
                "hot_topics": [],
                "sentiment_analysis": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                },
                "keyword_analysis": [],
                "suggestions": []
            }
        
        # 基础统计（保持原有逻辑）
        total_reviews = len(reviews)
        ratings = [r.get('rating', 0) for r in reviews]
        average_rating = sum(ratings) / total_reviews if total_reviews > 0 else 0
        
        # 情感分析
        positive_count = len([r for r in reviews if r.get('rating', 0) >= 4])
        neutral_count = len([r for r in reviews if r.get('rating', 0) == 3])
        negative_count = len([r for r in reviews if r.get('rating', 0) <= 2])
        
        positive_rate = positive_count / total_reviews * 100 if total_reviews > 0 else 0
        negative_rate = negative_count / total_reviews * 100 if total_reviews > 0 else 0
        
        # 时间趋势分析（保持原有逻辑）
        trends = self._analyze_trends(reviews)
        
        # 使用AI进行深度分析
        ai_analysis = await self._ai_deep_analysis(reviews)
        
        return {
            "summary": {
                "total_reviews": total_reviews,
                "average_rating": round(average_rating, 1),
                "positive_rate": round(positive_rate, 1),
                "negative_rate": round(negative_rate, 1)
            },
            "trends": trends,
            "hot_topics": ai_analysis.get("hot_topics", []),
            "sentiment_analysis": {
                "positive": positive_count,
                "neutral": neutral_count,
                "negative": negative_count
            },
            "keyword_analysis": ai_analysis.get("keyword_analysis", []),
            "suggestions": ai_analysis.get("suggestions", [])
        }
    
    async def _ai_deep_analysis(self, reviews: List[Dict]) -> Dict[str, Any]:
        """使用DeepSeek API进行深度分析"""
        
        # 如果没有配置API密钥，使用备用分析
        if not self.api_key:
            print("DeepSeek API密钥未配置，使用备用分析")
            return self._fallback_analysis(reviews)
        
        # 构建评价数据文本
        reviews_text = self._build_reviews_text(reviews)
        
        prompt = f"""你是一位专业的餐饮服务质量分析专家。请对以下老年社区助餐服务的用户评价进行深度分析。

【评价数据】
{reviews_text}

请提供以下分析结果，以JSON格式返回：

{{
    "hot_topics": [
        {{
            "topic": "话题名称（如：配送服务、餐品口味、分量等）",
            "count": 提及次数,
            "percentage": 占比百分比,
            "type": "positive或negative",
            "examples": [
                {{
                    "content": "具体评价内容摘录",
                    "rating": 评分,
                    "time": "评价时间"
                }}
            ]
        }}
    ],
    "keyword_analysis": [
        {{
            "category": "关键词类别（如：口味、服务、配送等）",
            "count": 出现次数
        }}
    ],
    "suggestions": [
        "具体的改进建议1",
        "具体的改进建议2"
    ]
}}

分析要求：
1. 热点话题要具体，不要泛泛而谈
2. 每个话题提供2-3个真实的评价示例
3. 改进建议要针对性强，可操作
4. 必须返回合法的JSON格式
"""
        
        try:
            print(f"正在调用DeepSeek API进行评价分析...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    },
                    timeout=60.0
                )
                
                print(f"API响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    print("AI分析完成，正在解析结果...")
                    
                    # 解析JSON响应
                    return self._parse_ai_response(ai_response, reviews)
                else:
                    error_detail = response.text
                    print(f"AI分析失败: {error_detail}")
                    return self._fallback_analysis(reviews)
                    
        except Exception as e:
            import traceback
            print(f"AI分析异常: {str(e)}")
            print(f"异常堆栈:\n{traceback.format_exc()}")
            return self._fallback_analysis(reviews)
    
    def _build_reviews_text(self, reviews: List[Dict]) -> str:
        """构建评价数据文本"""
        text_parts = []
        
        # 按评分分组
        positive_reviews = [r for r in reviews if r.get('rating', 0) >= 4]
        neutral_reviews = [r for r in reviews if r.get('rating', 0) == 3]
        negative_reviews = [r for r in reviews if r.get('rating', 0) <= 2]
        
        text_parts.append(f"总评价数: {len(reviews)}")
        text_parts.append(f"好评数: {len(positive_reviews)}")
        text_parts.append(f"中评数: {len(neutral_reviews)}")
        text_parts.append(f"差评数: {len(negative_reviews)}")
        text_parts.append("")
        
        # 添加具体评价内容（限制数量避免token过多）
        text_parts.append("【好评示例】")
        for i, review in enumerate(positive_reviews[:5]):
            text_parts.append(f"{i+1}. 评分: {review.get('rating')} - {review.get('content', '')}")
        
        text_parts.append("")
        text_parts.append("【差评示例】")
        for i, review in enumerate(negative_reviews[:5]):
            text_parts.append(f"{i+1}. 评分: {review.get('rating')} - {review.get('content', '')}")
        
        text_parts.append("")
        text_parts.append("【中评示例】")
        for i, review in enumerate(neutral_reviews[:3]):
            text_parts.append(f"{i+1}. 评分: {review.get('rating')} - {review.get('content', '')}")
        
        return "\n".join(text_parts)
    
    def _parse_ai_response(self, ai_response: str, reviews: List[Dict]) -> Dict[str, Any]:
        """解析AI返回的JSON响应"""
        try:
            # 清理可能的markdown代码块标记
            cleaned_response = ai_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            cleaned_response = cleaned_response.strip()
            
            # 解析JSON
            result = json.loads(cleaned_response)
            
            # 确保必要的字段存在
            if "hot_topics" not in result:
                result["hot_topics"] = []
            if "keyword_analysis" not in result:
                result["keyword_analysis"] = []
            if "suggestions" not in result:
                result["suggestions"] = []
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {str(e)}")
            print(f"原始响应: {ai_response}")
            return self._fallback_analysis(reviews)
    
    def _fallback_analysis(self, reviews: List[Dict]) -> Dict[str, Any]:
        """备用分析方案（当AI API不可用时使用）"""
        print("使用备用分析方案...")
        
        # 关键词分析
        keywords = self._extract_keywords(reviews)
        
        # 热点话题分析
        hot_topics = self._analyze_hot_topics(keywords, reviews)
        
        # 改进建议
        ratings = [r.get('rating', 0) for r in reviews]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        positive_count = len([r for r in reviews if r.get('rating', 0) >= 4])
        positive_rate = positive_count / len(reviews) * 100 if reviews else 0
        negative_count = len([r for r in reviews if r.get('rating', 0) <= 2])
        negative_rate = negative_count / len(reviews) * 100 if reviews else 0
        
        suggestions = self._generate_suggestions(hot_topics, positive_rate, negative_rate, average_rating)
        
        return {
            "hot_topics": hot_topics,
            "keyword_analysis": keywords,
            "suggestions": suggestions
        }
    
    @staticmethod
    def _extract_keywords(reviews: List[Dict]) -> List[Dict]:
        """提取关键词"""
        content_list = [r.get('content', '') for r in reviews if r.get('content')]
        
        # 定义关键词词典
        keywords_dict = {
            '口味': ['味道', '好吃', '美味', '可口', '香', '甜', '咸', '辣', '淡', '酸'],
            '服务': ['服务', '态度', '热情', '礼貌', '耐心', '周到'],
            '配送': ['配送', '快递', '送达', '准时', '速度', '慢', '快'],
            '包装': ['包装', '盒子', '袋子', '完好', '破损', '干净'],
            '价格': ['价格', '贵', '便宜', '实惠', '性价比'],
            '分量': ['分量', '量', '少', '多', '足够', '不够'],
            '新鲜': ['新鲜', '新鲜度', '新鲜的', '不新鲜'],
            '卫生': ['卫生', '干净', '脏', '卫生问题'],
            '营养': ['营养', '健康', '营养丰富', '健康饮食']
        }
        
        keyword_counts = defaultdict(int)
        
        for content in content_list:
            for category, keywords in keywords_dict.items():
                for keyword in keywords:
                    if keyword in content:
                        keyword_counts[category] += 1
        
        # 转换为排序后的列表
        keyword_list = [
            {"category": category, "count": count}
            for category, count in keyword_counts.items()
        ]
        
        return sorted(keyword_list, key=lambda x: x['count'], reverse=True)
    
    @staticmethod
    def _analyze_hot_topics(keywords: List[Dict], reviews: List[Dict]) -> List[Dict]:
        """分析热点话题"""
        hot_topics = []
        
        # 分析负面评价中的热点问题
        negative_reviews = [r for r in reviews if r.get('rating', 0) <= 2]
        
        if negative_reviews:
            # 常见问题模式
            problem_patterns = {
                '配送延迟': ['慢', '迟到', '超时', '长时间'],
                '餐品质量': ['凉', '冷', '不新鲜', '变质', '难吃'],
                '服务态度': ['态度差', '不礼貌', '不耐烦'],
                '分量不足': ['分量少', '不够吃', '太少'],
                '价格过高': ['太贵', '不值', '价格高']
            }
            
            for problem, patterns in problem_patterns.items():
                count = 0
                examples = []
                
                for review in negative_reviews:
                    content = review.get('content', '')
                    if any(pattern in content for pattern in patterns):
                        count += 1
                        if len(examples) < 3:
                            examples.append({
                                "content": content[:100] + "..." if len(content) > 100 else content,
                                "rating": review.get('rating', 0),
                                "time": review.get('created_at')
                            })
                
                if count > 0:
                    hot_topics.append({
                        "topic": problem,
                        "count": count,
                        "percentage": round(count / len(negative_reviews) * 100, 1),
                        "examples": examples
                    })
        
        # 添加正面热点话题
        positive_reviews = [r for r in reviews if r.get('rating', 0) >= 4]
        
        if positive_reviews:
            positive_patterns = {
                '配送及时': ['快', '准时', '及时'],
                '餐品美味': ['好吃', '美味', '可口'],
                '服务好': ['态度好', '热情', '周到'],
                '包装完好': ['包装好', '完好', '干净']
            }
            
            for topic, patterns in positive_patterns.items():
                count = 0
                
                for review in positive_reviews:
                    content = review.get('content', '')
                    if any(pattern in content for pattern in patterns):
                        count += 1
                
                if count > 5:  # 只显示比较热门的正面话题
                    hot_topics.append({
                        "topic": topic,
                        "count": count,
                        "percentage": round(count / len(positive_reviews) * 100, 1),
                        "type": "positive"
                    })
        
        return sorted(hot_topics, key=lambda x: x['count'], reverse=True)
    
    @staticmethod
    def _analyze_trends(reviews: List[Dict]) -> List[Dict]:
        """分析时间趋势"""
        # 按日期分组
        daily_data = defaultdict(lambda: {
            'count': 0,
            'total_rating': 0,
            'positive': 0,
            'negative': 0
        })
        
        for review in reviews:
            created_at = review.get('created_at')
            if created_at:
                date_str = created_at.split('T')[0] if isinstance(created_at, str) else created_at.strftime('%Y-%m-%d')
                rating = review.get('rating', 0)
                
                daily_data[date_str]['count'] += 1
                daily_data[date_str]['total_rating'] += rating
                
                if rating >= 4:
                    daily_data[date_str]['positive'] += 1
                elif rating <= 2:
                    daily_data[date_str]['negative'] += 1
        
        # 转换为趋势数据
        trends = []
        for date_str, data in sorted(daily_data.items()):
            avg_rating = data['total_rating'] / data['count'] if data['count'] > 0 else 0
            trends.append({
                "date": date_str,
                "count": data['count'],
                "average_rating": round(avg_rating, 1),
                "positive_count": data['positive'],
                "negative_count": data['negative']
            })
        
        return trends[-7:]  # 返回最近7天的数据
    
    @staticmethod
    def _generate_suggestions(hot_topics: List[Dict], positive_rate: float, negative_rate: float, average_rating: float) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 基于热点问题生成建议
        problem_topics = [topic for topic in hot_topics if 'type' not in topic or topic['type'] != 'positive']
        
        if problem_topics:
            if any(t['topic'] == '配送延迟' for t in problem_topics):
                suggestions.append("优化配送流程，考虑增加配送人员或调整配送路线，减少配送延迟")
            
            if any(t['topic'] == '餐品质量' for t in problem_topics):
                suggestions.append("加强餐品质量监控，确保餐品新鲜度和温度，定期检查食材质量")
            
            if any(t['topic'] == '服务态度' for t in problem_topics):
                suggestions.append("加强服务人员培训，提升服务态度和专业素养")
            
            if any(t['topic'] == '分量不足' for t in problem_topics):
                suggestions.append("评估餐品分量，确保满足顾客需求，考虑适当增加分量")
        
        # 基于整体评分生成建议
        if average_rating < 3.5:
            suggestions.append("整体评分较低，建议全面提升服务质量，重点关注顾客反馈的问题")
        
        if negative_rate > 20:
            suggestions.append(f"差评率较高（{negative_rate}%），需要重点分析差评原因并采取改进措施")
        
        if positive_rate > 80:
            suggestions.append("好评率较高，继续保持良好的服务质量，同时关注少数差评的改进")
        
        # 通用建议
        suggestions.append("定期收集和分析顾客反馈，建立反馈响应机制，及时解决顾客问题")
        suggestions.append("考虑推出会员福利或优惠活动，提升顾客满意度和忠诚度")
        
        return suggestions[:5]  # 返回前5条最重要的建议
