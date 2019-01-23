\version "2.18.2"
\language "english"
% O67_score.ly - Score for Symphony No. 5

#(ly:set-option 'relative-includes #t)
\include "defs.ily"

\header {
  instrument = "Score"
}

\book {
  \score { % Movement 1
    \header {
      opus = "Op. 67"
    }
    <<
    \new Staff = "flute" \with {
      instrumentName = "Flute I"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \global_first_mov
          \flute_one_first_mov
        >>
      }
    }
    \new Staff = "flute" \with {
      instrumentName = "Flute II"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \flute_two_first_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe I"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_one_first_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe II"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_two_first_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet I"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_one_first_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet II"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_two_first_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon I"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_one_first_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon II"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_two_first_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn I"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_one_first_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn II"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_two_first_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet I"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_one_first_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet II"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_two_first_mov
        >>
      }
    }
    \new Staff = "timpani" \with {
      instrumentName = "Timpani"
      shortInstrumentName = "Timp"
      midiInstrument = #"timpani"
    } {
      \new Voice  {
        <<
          \timpani_first_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin I"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_one_first_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin II"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_two_first_mov
        >>
      }
    }
    \new Staff = "viola" \with {
      instrumentName = "Viola"
      shortInstrumentName = "Vla."
      midiInstrument = #"viola"
    } {
      \new Voice  {
        <<
          \viola_first_mov
        >>
      }
    }
    \new Staff = "violoncello" \with {
      instrumentName = "Violoncello"
      shortInstrumentName = "Vc."
      midiInstrument = #"cello"
    } {
      \new Voice  {
        <<
          \violoncello_first_mov
        >>
      }
    }
    \new Staff = "contrabass" \with {
      instrumentName = "Contrabass"
      shortInstrumentName = "Cb."
      midiInstrument = #"contrabass"
    } {
      \new Voice  {
        <<
          \contrabass_first_mov
        >>
      }
    }
    >>
  \layout {
  }
  \midi {
  }
  }

  \score { % Movement 2
    <<
    \new Staff = "flute" \with {
      instrumentName = "Flute I"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \global_second_mov
          \flute_one_second_mov
        >>
      }
    }
    \new Staff = "flute" \with {
      instrumentName = "Flute II"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \flute_two_second_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe I"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_one_second_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe II"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_two_second_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet I"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_one_second_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet II"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_two_second_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon I"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_one_second_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon II"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_two_second_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn I"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_one_second_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn II"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_two_second_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet I"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_one_second_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet II"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_two_second_mov
        >>
      }
    }
    \new Staff = "timpani" \with {
      instrumentName = "Timpani"
      shortInstrumentName = "Timp"
      midiInstrument = #"timpani"
    } {
      \new Voice  {
        <<
          \timpani_second_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin I"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_one_second_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin II"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_two_second_mov
        >>
      }
    }
    \new Staff = "viola" \with {
      instrumentName = "Viola"
      shortInstrumentName = "Vla."
      midiInstrument = #"viola"
    } {
      \new Voice  {
        <<
          \viola_second_mov
        >>
      }
    }
    \new Staff = "violoncello" \with {
      instrumentName = "Violoncello"
      shortInstrumentName = "Vc."
      midiInstrument = #"cello"
    } {
      \new Voice  {
        <<
          \violoncello_second_mov
        >>
      }
    }
    \new Staff = "contrabass" \with {
      instrumentName = "Contrabass"
      shortInstrumentName = "Cb."
      midiInstrument = #"contrabass"
    } {
      \new Voice  {
        <<
          \contrabass_second_mov
        >>
      }
    }
    >>
  \layout {
  }
  \midi {
  }
  }

  \score { % Movement 3
    <<
    \new Staff = "flute" \with {
      instrumentName = "Flute I"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \global_third_mov
          \flute_one_third_mov
        >>
      }
    }
    \new Staff = "flute" \with {
      instrumentName = "Flute II"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \flute_two_third_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe I"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_one_third_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe II"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_two_third_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet I"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_one_third_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet II"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_two_third_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon I"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_one_third_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon II"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_two_third_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn I"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_one_third_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn II"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_two_third_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet I"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_one_third_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet II"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_two_third_mov
        >>
      }
    }
    \new Staff = "timpani" \with {
      instrumentName = "Timpani"
      shortInstrumentName = "Timp"
      midiInstrument = #"timpani"
    } {
      \new Voice  {
        <<
          \timpani_third_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin I"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_one_third_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin II"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_two_third_mov
        >>
      }
    }
    \new Staff = "viola" \with {
      instrumentName = "Viola"
      shortInstrumentName = "Vla."
      midiInstrument = #"viola"
    } {
      \new Voice  {
        <<
          \viola_third_mov
        >>
      }
    }
    \new Staff = "violoncello" \with {
      instrumentName = "Violoncello"
      shortInstrumentName = "Vc."
      midiInstrument = #"cello"
    } {
      \new Voice  {
        <<
          \violoncello_third_mov
        >>
      }
    }
    \new Staff = "contrabass" \with {
      instrumentName = "Contrabass"
      shortInstrumentName = "Cb."
      midiInstrument = #"contrabass"
    } {
      \new Voice  {
        <<
          \contrabass_third_mov
        >>
      }
    }
    >>
  \layout {
  }
  \midi {
  }
  }

  \score { % Movement 4
    <<
    \new Staff = "flute" \with {
      instrumentName = "Flute I"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \global_fourth_mov
          \flute_one_fourth_mov
        >>
      }
    }
    \new Staff = "flute" \with {
      instrumentName = "Flute II"
      shortInstrumentName = "Fl."
      midiInstrument = #"flute"
    } {
      \new Voice  {
        <<
          \flute_two_fourth_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe I"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_one_fourth_mov
        >>
      }
    }
    \new Staff = "oboe" \with {
      instrumentName = "Oboe II"
      shortInstrumentName = "Ob."
      midiInstrument = #"oboe"
    } {
      \new Voice  {
        <<
          \oboe_two_fourth_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet I"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_one_fourth_mov
        >>
      }
    }
    \new Staff = "clarinet_in_bb" \with {
      instrumentName = "Clarinet II"
      shortInstrumentName = "Cl."
      midiInstrument = #"clarinet"
    } {
      \new Voice  {
        <<
          \clarinet_in_bb_two_fourth_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon I"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_one_fourth_mov
        >>
      }
    }
    \new Staff = "bassoon" \with {
      instrumentName = "Bassoon II"
      shortInstrumentName = "Bsn."
      midiInstrument = #"bassoon"
    } {
      \new Voice  {
        <<
          \bassoon_two_fourth_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn I"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_one_fourth_mov
        >>
      }
    }
    \new Staff = "french_horn" \with {
      instrumentName = "French Horn II"
      shortInstrumentName = "Hn."
      midiInstrument = #"french horn"
    } {
      \new Voice  {
        <<
          \french_horn_two_fourth_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet I"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_one_fourth_mov
        >>
      }
    }
    \new Staff = "trumpet_in_c" \with {
      instrumentName = "Trumpet II"
      shortInstrumentName = "Tpt."
      midiInstrument = #"trumpet"
    } {
      \new Voice  {
        <<
          \trumpet_in_c_two_fourth_mov
        >>
      }
    }
    \new Staff = "timpani" \with {
      instrumentName = "Timpani"
      shortInstrumentName = "Timp"
      midiInstrument = #"timpani"
    } {
      \new Voice  {
        <<
          \timpani_fourth_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin I"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_one_fourth_mov
        >>
      }
    }
    \new Staff = "violin" \with {
      instrumentName = "Violin II"
      shortInstrumentName = "Vln."
      midiInstrument = #"violin"
    } {
      \new Voice  {
        <<
          \violin_two_fourth_mov
        >>
      }
    }
    \new Staff = "viola" \with {
      instrumentName = "Viola"
      shortInstrumentName = "Vla."
      midiInstrument = #"viola"
    } {
      \new Voice  {
        <<
          \viola_fourth_mov
        >>
      }
    }
    \new Staff = "violoncello" \with {
      instrumentName = "Violoncello"
      shortInstrumentName = "Vc."
      midiInstrument = #"cello"
    } {
      \new Voice  {
        <<
          \violoncello_fourth_mov
        >>
      }
    }
    \new Staff = "contrabass" \with {
      instrumentName = "Contrabass"
      shortInstrumentName = "Cb."
      midiInstrument = #"contrabass"
    } {
      \new Voice  {
        <<
          \contrabass_fourth_mov
        >>
      }
    }
    >>
  \layout {
  }
  \midi {
  }
  }

  \paper {
  }
}

