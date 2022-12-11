# le4-audio-kuis (private)

京都大学 工学部 情報学科 計算機科学実験及演習4 音響信号処理 のサンプルソースコードです。

簡易カラオケシステムを作成します。

## Files & Directories
- `src`
  - `plot_waveform.py`: 音声から波形図を作成
  - `plot_spectrum.py`: 音声からスペクトル図を作成
  - `plot_spectrogram.py`: 音声からスペクトログラムを作成

## usage of SOX
- 録音：`sox -r 16k -b 16 -c 1 -d output.wav trim 0 10`
- 再生：`sox input.wav -d`