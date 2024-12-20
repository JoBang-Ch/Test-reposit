from pydub import AudioSegment
from tkinter import Tk, filedialog, Label, Entry, Button, messagebox
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
        messagebox.showinfo("완료", f"속도 조정된 파일이 저장되었습니다: {output_file}")
    
    except FileNotFoundError:
        # 입력 파일이 존재하지 않을 때의 예외 처리
        error_message = f"파일을 찾을 수 없습니다: {input_file}"
        messagebox.showerror("오류", error_message)
        logging.error(error_message)
    
    except Exception as e:
        # 기타 예외 처리
        error_message = f"오류 발생: {str(e)}"
        messagebox.showerror("오류", error_message)
        logging.error(error_message)

def select_file():
    """파일 탐색기에서 파일을 선택합니다."""
    file_path = filedialog.askopenfilename(
        title="오디오 파일 선택",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")]
    )
    input_path_entry.delete(0, "end")
    input_path_entry.insert(0, file_path)

def process_audio():
    """GUI를 통해 입력받은 정보를 바탕으로 오디오 처리"""
    input_file = input_path_entry.get()
    speed_factor = speed_entry.get()
    
    if not input_file:
        messagebox.showerror("오류", "오디오 파일을 선택하세요.")
        return
    
    try:
        speed_factor = float(speed_factor)
        if speed_factor <= 0:
            raise ValueError("배속 값은 0보다 커야 합니다.")
    except ValueError as ve:
        messagebox.showerror("오류", f"잘못된 배속 값: {ve}")
        return

    # 출력 파일 이름 설정 (배속 값 포함)
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_sped_up_{speed_factor}x{ext}"
    
    # 속도 조정 함수 호출
    adjust_audio_speed(input_file, speed_factor, output_file)

# Tkinter GUI 설정
root = Tk()
root.title("Sped up Maker")
root.geometry("400x200")

# GUI 구성 요소
Label(root, text="오디오 파일 경로:").pack(pady=5)
input_path_entry = Entry(root, width=50)
input_path_entry.pack(pady=5)
Button(root, text="파일 선택", command=select_file).pack(pady=5)

Label(root, text="배속 값 (예: 1.5):").pack(pady=5)
speed_entry = Entry(root, width=10)
speed_entry.pack(pady=5)

Button(root, text="처리 시작", command=process_audio).pack(pady=20)

# GUI 실행
root.mainloop()
