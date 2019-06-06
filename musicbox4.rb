# musicbox1 0.211



track4 = "c5,d5,b4,  ,g5,e5,c5,  "
track3 = "  ,cb4, ,e4,g2,  "
track2 = "  ,57,  ,43,  ,52"
track1 = "45,  ,55,  ,55,  "

beat1 = 0.26

t4stop = 0
t3stop = 0
t2stop = 0
t1stop = 0

live_loop :t4 do track4.split(',').each do |i|
    n = i.gsub(/\s+/, '')
    play stop if t4stop == 1
    use_synth :dsaw
    begin
      play n, amp: 0.55, release: beat1 * 1.1 if n != ''
    rescue
      play n.to_i if n != ''
    rescue
      print n
      print 'bad note'
    end
    sleep beat1 * 1.5
end end

live_loop :t3 do track3.split(',').each do |i|
    n = i.gsub(/\s+/, '')
    play stop if t3stop == 1
    use_synth :dsaw
    begin
      play i, amp: 0.8, release: beat1 * 1 if n != ''
    rescue
      print i
      print 'bad note'
    end
    sleep beat1
end end

live_loop :t2 do track2.split(',').each do |i|
    n = i.gsub(/\s+/, '')
    play stop if t2stop == 1
    beat2 = beat1
    use_synth :subpulse
    begin
      play i.to_i if n != ''
    rescue
    end
    sleep beat2
end end

live_loop :t1 do track1.split(',').each do |i|
    n = i.gsub(/\s+/, '')
    play stop if t1stop == 1
    # sync :t2
    # sync :t3
    use_synth :subpulse
    begin
      play i.to_i if n != ''
    rescue
    end
    sleep beat1
end end