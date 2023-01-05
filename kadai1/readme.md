# 課題１「音響信号可視化 GUI」
音響信号ファイルを読み込み，音響信号のさまざまな情報を表示するグラフィカルユーザーインタフェースを作成せよ.  
少なくとも以下の3つを同時に表示させること.
  1. 音響信号のスペクトログラム
  2. 音響信号の基本周波数
  3. 母音などの何らかの識別を行った結果

そのうえで，このインタフェースがより便利なものになるように改良せよ. 例えば以下のような改良が考えられるが，もちろんこれ以外の改良でも構わない.  
創意工夫すること.
- 音響信号の区間を選択し，その区間のスペクトルを表示する.
- 音響信号を再生し，その再生位置をアニメーションで示す.
- 音楽音響信号のコードとその区間を認識し表示する.
- NMFを用いて，音声と音楽を分離し，選択的に再生する.


## Files & Directories
- `gui.py`: Toplevel
- `src`
  + `process.py`: Main function to analyze original data.
  + `melody_funs.py`: Functions for estimate fundamental frequency.
  + `speech_model.py`: Functions for speech recognition. Parameters of this module are stored in `ex16/mu_sigma_result.pickle`.


## Reference
- [PyAudioでの再生停止 (stack overflow)](https://stackoverflow.com/questions/33851107/tkinter-button-calling-function-to-play-wave-with-pyaudio-crashes)
- [Pyaudioでwavファイルを再生（ブログ）](https://shizenkarasuzon.hatenablog.com/entry/2018/12/31/145510)
- [waveのドキュメント](https://docs.python.org/ja/3/library/wave.html#wave.Wave_read.readframes)
