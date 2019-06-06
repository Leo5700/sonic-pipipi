# musicbox5 0.2

# track4 = 'c5,d5,b4,  ,g5,e5,c5,  '
track4 = 'c4,55,b3,  ,g4,e4,c4,  '
track3 = '  ,cb4, ,e4,g2,  '
track2 = '  ,57,  ,43,  ,52'
track1 = '45,  ,55,  ,55,  '
track0 = '  ,  ,  ,  ,  ,  '

beat0= 0.2

def prepare (track)
  sync :track0
  a = track.split(',')
  b = a.map{|x| x.gsub(/\s+/, '')}
  c = []
  b.each do |x|
    if x == '' then
      c << :r
    elsif !/\A\d+\z/.match(x) then
      c << x
    else
      c << x.to_i
    end
  end
  return c
end

live_loop :t4 do
  stop if not defined? track4
  prepare(track4).each do |n|
    use_synth :dsaw
    play n, amp: 0.55, release: beat0 * 1.1
    sleep beat0 * 1.5
end end

live_loop :t3 do
  stop if not defined? track3
  prepare(track3).each do |n|
    use_synth :dsaw
    play n, amp: 0.55, release: beat0 * 1.1
    sleep beat0
end end

live_loop :t2 do
  stop if not defined? track2
  prepare(track2).each do |n|
    use_synth :subpulse
    play n, amp: 0.55, release: beat0 * 1.1
    sleep beat0
end end

live_loop :t1 do
  stop if not defined? track1
  prepare(track1).each do |n|
    use_synth :subpulse
    play n, amp: 0.55, release: beat0 * 1.1
    sleep beat0
end end

live_loop :track0 do
  track0.split(',').each do |i| n = i.gsub(/\s+/, '')
    sleep beat0
end end