import os
import uuid
import dashscope
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.voice_synthesis import VoiceSynthesis

# 确保加载环境变量
from dotenv import load_dotenv
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(project_root, ".env")
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# 导入Piper TTS
try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
    print("Piper TTS imported successfully")
except ImportError as e:
    PIPER_AVAILABLE = False
    print(f"Piper TTS import failed: {e}")
    print("Piper TTS not available, falling back to DashScope")


class VoiceService:
    # Piper TTS配置
    @classmethod
    def get_piper_model_path(cls):
        return os.getenv("PIPER_MODEL_PATH", os.path.join(project_root, "models", "piper", "zh_CN-huayan-medium.onnx"))
    
    @classmethod
    def get_piper_config_path(cls):
        return os.getenv("PIPER_CONFIG_PATH", os.path.join(project_root, "models", "piper", "zh_CN-huayan-medium.onnx.json"))
    
    # DashScope TTS配置（动态获取环境变量）
    @classmethod
    def get_dashscope_api_key(cls):
        return os.getenv("DASHSCOPE_API_KEY", "")
    
    @classmethod
    def get_dashscope_api_url(cls):
        return os.getenv("DASHSCOPE_API_URL", "https://dashscope.aliyuncs.com/api/v1")
    
    @classmethod
    def get_dashscope_tts_model(cls):
        return os.getenv("DASHSCOPE_TTS_MODEL", "qwen3-tts-flash")
    
    @classmethod
    def get_dashscope_tts_voice(cls):
        return os.getenv("DASHSCOPE_TTS_VOICE", "Cherry")
    
    @classmethod
    def get_dashscope_tts_speed(cls):
        return float(os.getenv("DASHSCOPE_TTS_SPEED", "0.8"))
    
    @classmethod
    def get_dashscope_tts_language(cls):
        return os.getenv("DASHSCOPE_TTS_LANGUAGE", "zh_CN")
    
    # Piper TTS语音合成方法
    @classmethod
    def synthesize_with_piper(cls, text_content: str, speed: float = 0.8) -> str:
        """使用Piper TTS进行本地语音合成"""
        try:
            model_path = cls.get_piper_model_path()
            config_path = cls.get_piper_config_path()
            
            print(f"使用Piper TTS，模型路径: {model_path}")
            print(f"配置文件路径: {config_path}")
            
            # 检查模型文件是否存在
            print(f"模型文件存在: {os.path.exists(model_path)}")
            print(f"配置文件存在: {os.path.exists(config_path)}")
            
            if not os.path.exists(model_path) or not os.path.exists(config_path):
                print("Piper TTS模型文件不存在")
                raise ValueError("Piper TTS模型文件不存在，请先下载模型")
            
            # 初始化Piper Voice
            print("开始加载Piper Voice模型...")
            voice = PiperVoice.load(model_path, config_path)
            print("Piper Voice模型加载成功")
            
            # 生成音频文件名
            audio_filename = f"voice_{uuid.uuid4().hex}.wav"
            audio_path = os.path.join("static", "voices", audio_filename)
            print(f"音频文件路径: {audio_path}")
            
            # 确保目录存在
            os.makedirs(os.path.join("static", "voices"), exist_ok=True)
            print("目录创建成功")
            
            # 合成语音
            print(f"开始合成语音，文本: {text_content[:50]}...")
            
            # 收集所有音频数据
            audio_data = b""
            for audio_chunk in voice.synthesize(text_content):
                audio_data += audio_chunk.audio_int16_bytes
            
            print(f"音频数据长度: {len(audio_data)} 字节")
            
            # 添加WAV文件头
            sample_rate = 22050  # Piper TTS默认采样率
            num_channels = 1     # 单声道
            bits_per_sample = 16  # 16位
            
            # 计算WAV文件头
            data_size = len(audio_data)
            file_size = 44 + data_size
            
            # WAV文件头
            wav_header = b""
            wav_header += b"RIFF"  # ChunkID
            wav_header += (file_size - 8).to_bytes(4, 'little')  # ChunkSize
            wav_header += b"WAVE"  # Format
            wav_header += b"fmt "  # Subchunk1ID
            wav_header += (16).to_bytes(4, 'little')  # Subchunk1Size (PCM)
            wav_header += (1).to_bytes(2, 'little')  # AudioFormat (PCM)
            wav_header += (num_channels).to_bytes(2, 'little')  # NumChannels
            wav_header += (sample_rate).to_bytes(4, 'little')  # SampleRate
            wav_header += (sample_rate * num_channels * bits_per_sample // 8).to_bytes(4, 'little')  # ByteRate
            wav_header += (num_channels * bits_per_sample // 8).to_bytes(2, 'little')  # BlockAlign
            wav_header += (bits_per_sample).to_bytes(2, 'little')  # BitsPerSample
            wav_header += b"data"  # Subchunk2ID
            wav_header += (data_size).to_bytes(4, 'little')  # Subchunk2Size
            
            # 写入文件
            with open(audio_path, "wb") as f:
                f.write(wav_header)
                f.write(audio_data)
            
            print("语音合成完成，已添加WAV文件头")
            
            # 生成可访问的URL
            voice_url = f"/static/voices/{audio_filename}"
            print(f"Piper TTS语音合成成功，语音文件: {voice_url}")
            
            return voice_url
            
        except Exception as e:
            print(f"Piper TTS语音合成失败: {e}")
            import traceback
            traceback.print_exc()
            raise ValueError(f"Piper TTS语音合成失败: {str(e)}")
    
    @staticmethod
    def get_user_voice_records(db: Session, user_id: int):
        """获取用户的语音合成记录"""
        return db.query(VoiceSynthesis).filter(
            VoiceSynthesis.user_id == user_id
        ).order_by(VoiceSynthesis.created_at.desc()).all()
    
    @staticmethod
    def create_voice_synthesis(
        db: Session,
        user_id: int,
        text_content: str,
        voice_type: str = "elderly",
        language: str = "zh_CN",
        speed: float = 0.8
    ) -> VoiceSynthesis:
        """创建语音合成记录"""
        voice_record = VoiceSynthesis(
            user_id=user_id,
            text_content=text_content,
            voice_type=voice_type,
            language=language,
            speed=speed,
            status="pending"
        )
        db.add(voice_record)
        db.commit()
        db.refresh(voice_record)
        return voice_record
    
    @classmethod
    async def synthesize_speech(
        cls,
        db: Session,
        record_id: int,
        text_content: str,
        voice_type: str = None,
        language: str = None,
        speed: float = None
    ) -> str:
        """合成语音并返回语音URL，优先使用Piper TTS，失败则回退到DashScope"""
        default_speed = cls.get_dashscope_tts_speed()
        final_speed = speed or default_speed
        
        print(f"开始语音合成，文本内容: {text_content[:50]}...")
        
        # 更新状态为处理中
        voice_record = db.query(VoiceSynthesis).filter(
            VoiceSynthesis.id == record_id
        ).first()
        
        if voice_record:
            voice_record.status = "processing"
            db.commit()
        
        try:
            # 优先使用Piper TTS进行本地语音合成
            print(f"当前PIPER_AVAILABLE值: {PIPER_AVAILABLE}")
            print(f"PIPER_AVAILABLE类型: {type(PIPER_AVAILABLE)}")
            
            # 直接尝试使用Piper TTS，不依赖PIPER_AVAILABLE标志
            print("直接尝试使用Piper TTS进行本地语音合成")
            try:
                print(f"准备调用synthesize_with_piper，文本: {text_content[:30]}...")
                voice_url = cls.synthesize_with_piper(text_content, final_speed)
                print(f"Piper TTS调用成功，voice_url: {voice_url}")
                
                # 更新状态为已完成
                if voice_record:
                    voice_record.voice_url = voice_url
                    voice_record.status = "completed"
                    voice_record.completed_at = datetime.utcnow()
                    db.commit()
                
                return voice_url
            except Exception as piper_error:
                print(f"Piper TTS语音合成失败，尝试回退到DashScope: {piper_error}")
                import traceback
                traceback.print_exc()
            
            # Piper TTS不可用或失败，回退到DashScope
            print("使用DashScope TTS进行语音合成")
            api_key = cls.get_dashscope_api_key()
            api_url = cls.get_dashscope_api_url()
            tts_model = cls.get_dashscope_tts_model()
            default_voice = cls.get_dashscope_tts_voice()
            default_language = cls.get_dashscope_tts_language()
            
            print(f"DASHSCOPE_API_KEY: {api_key}")
            print(f"DASHSCOPE_API_URL: {api_url}")
            print(f"DASHSCOPE_TTS_MODEL: {tts_model}")
            print(f"DASHSCOPE_TTS_VOICE: {default_voice}")
            print(f"DASHSCOPE_TTS_SPEED: {default_speed}")
            print(f"DASHSCOPE_TTS_LANGUAGE: {default_language}")
            
            # 检查API密钥是否配置
            if not api_key or api_key.strip() == "":
                print("DashScope API密钥未配置")
                raise ValueError("DashScope API密钥未配置，请在.env文件中配置有效的DASHSCOPE_API_KEY")
            
            # 配置DashScope
            dashscope.base_http_api_url = api_url
            
            # 直接使用.env文件中配置的音色，不再根据voice_type选择
            voice = default_voice
            
            # 调用DashScope TTS API
            print(f"使用声音: {voice}")
            print(f"使用语速: {final_speed}")
            
            # 使用SpeechSynthesizer接口
            response = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
                model=tts_model,
                api_key=api_key,
                text=text_content,
                voice=voice,
                format="mp3",
                speed=final_speed
            )
            
            print(f"DashScope响应: {response}")
            
            if response.status_code == 200 and response.output:
                audio_info = response.output.audio
                if audio_info:
                    if isinstance(audio_info, dict) and audio_info.get("url"):
                        # DashScope返回的是音频URL，直接使用
                        voice_url = audio_info["url"]
                        print(f"语音合成成功，语音URL: {voice_url}")
                        
                        # 更新状态为已完成
                        if voice_record:
                            voice_record.voice_url = voice_url
                            voice_record.status = "completed"
                            voice_record.completed_at = datetime.utcnow()
                            db.commit()
                        
                        return voice_url
                    elif isinstance(audio_info, bytes):
                        # 如果返回的是二进制数据，保存为文件
                        audio_filename = f"voice_{uuid.uuid4().hex}.mp3"
                        audio_path = os.path.join("static", "voices", audio_filename)
                        
                        # 确保目录存在
                        os.makedirs(os.path.join("static", "voices"), exist_ok=True)
                        
                        # 保存音频文件
                        with open(audio_path, "wb") as f:
                            f.write(audio_info)
                        
                        # 生成可访问的URL
                        voice_url = f"/static/voices/{audio_filename}"
                        print(f"语音合成成功，语音文件: {voice_url}")
                        
                        # 更新状态为已完成
                        if voice_record:
                            voice_record.voice_url = voice_url
                            voice_record.status = "completed"
                            voice_record.completed_at = datetime.utcnow()
                            db.commit()
                        
                        return voice_url
                    else:
                        print(f"音频数据格式不支持: {type(audio_info)}")
                        raise ValueError(f"音频数据格式不支持: {type(audio_info)}")
                else:
                    print("音频数据为空")
                    raise ValueError("音频数据为空")
            elif response.status_code == 401:
                print(f"DashScope API密钥无效: {response.status_code}")
                raise ValueError("DashScope API密钥无效，请检查.env文件中的DASHSCOPE_API_KEY配置")
            else:
                print(f"DashScope API调用失败: {response.status_code}")
                raise ValueError(f"DashScope API调用失败: {response.status_code}")
            
        except ValueError:
            # 更新状态为失败
            if voice_record:
                voice_record.status = "failed"
                db.commit()
            raise
        except Exception as e:
            print(f"语音合成异常: {e}")
            
            # 更新状态为失败
            if voice_record:
                voice_record.status = "failed"
                db.commit()
            
            raise ValueError(f"语音合成异常: {str(e)}")