# musicbox1 0.211

track2 = "--+---+"
track1 = "++--+-+-"

beat = 0.14

def cs (samplename)
  sample_path = "~/sonic-pipipi/samples"  ###
  return File.join(sample_path, samplename)
end

finishlen = beat * 2
ampall = 0.6

live_loop :t2 do
  track2.split('').each do |i|
    sample cs('test24.flac'), amp: ampall, finish: finishlen if i == '-'
    sample cs('test23.flac'), amp: ampall, finish: finishlen if i == '+'
    sleep beat * rrand(0.999, 1.001)
  end
end

live_loop :t1 do
  track1.split('').each do |i|
    sample cs('test22.flac'), amp: ampall, finish: finishlen if i == '-'
    sample cs('test21.flac'), amp: ampall, finish: finishlen if i == '+'
    sleep beat * rrand(0.999, 1.001)
  end
end


beatshift = 0.14
live_loop :beat do
  sleep beat * beatshift
  with_fx :echo, mix: 0.1, phase: 0.107 do
    sample :bass_hit_c, rate: 0.5, amp: 0.57
  end
  sleep beat * (4 - beatshift)
end
