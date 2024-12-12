from pydub import AudioSegment
from pydub.playback import play
import os
import logging

# 로그 파일 생성
log_file = "output_sped_up_log.txt"
logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(message)s')

def adjust_audio_speed(input_file, speed_factor, output_file):
    """
    오디오 파일을 읽어 속도를 조정한 후 저장합니다.
    
    :param input_file: 처리할 오디오 파일 경로 (str)
    :param speed_factor: 배속 값 (float, 1.0보다 큰 값은 빠르게, 작은 값은 느리게 재생)
    :param output_file: 저장될 파일 경로 (str)
    """
    try:
        # 오디오 파일 불러오기
        audio = AudioSegment.from_file(input_file)
        
        # 속도 조정 (배속)
        new_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed_factor)
        }).set_frame_rate(audio.frame_rate)
        
        # 조정된 오디오 저장
        new_audio.export(output_file, format="mp3")
        print(f"속도 조정된 파일이 저장되었습니다: {output_file}")
    
    except FileNotFoundError:
        # 입력 파일이 존재하지 않을 때의 예외 처리
        error_message = f"파일을 찾을 수 없습니다: {input_file}"
        print(error_message)
        logging.error(error_message)
    
    except Exception as e:
        # 기타 예외 처리
        error_message = f"오류 발생: {str(e)}"
        print(error_message)
        logging.error(error_message)

if __name__ == "__main__":
    # 사용자 입력 받기
    input_file = input("오디오 파일 경로를 입력하세요: ")  # 예: example.mp3
    try:
        speed_factor = float(input("배속 값을 입력하세요 (예: 1.5): "))  # 예: 1.5
        if speed_factor <= 0:
            raise ValueError("배속 값은 0보다 커야 합니다.")
    except ValueError as ve:
        print(f"잘못된 입력입니다: {ve}")
        logging.error(f"잘못된 배속 입력: {ve}")
        exit()
    
    # 출력 파일 이름 설정 (배속 값 포함)
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_sped_up_{speed_factor}x{ext}"
    
    # 속도 조정 함수 호출
    adjust_audio_speed(input_file, speed_factor, output_file)
