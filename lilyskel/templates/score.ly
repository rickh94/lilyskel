{% extends 'basepart.ly' %}
{%- block IDblock %}
% {{ filename }} - Score for {{ piece.headers.title }}
{%- endblock %}

{% block globalheader %}
  instrument = "Score"
{% endblock %}

{% block book %}
{%- for mov in piece.movements %}
  \score { % Movement {{ mov.num }}
    {%- if mov.num == 1 and piece.opus %}
    \header {
      opus = "{{ piece.opus }}"
    }
    {%- endif %}
    {%- for ins in instruments %}
    \new Staff = "{{ ins.name }}" \with {
      {%- if not ins.keyboard %}
      instrumentName = "{{ ins.part_name() }}"
      {%- if ins.abbr %}
      shortInstrumentName = "{{ ins.abbr }}"
      {%- endif %}
      {%- if ins.midi %}
      midiInstrument = #"{{ ins.midi }}"
      {%- endif %}
    } {
      \new Voice  {
        <<
          {%- if loop.index == 1 %}
          {{ lyglobal.var_name(mov.num) }}
          {%- endif %}
          {{ ins.var_name(mov.num) }}
        >>
      }
    }
    {%- elif ins.keyboard %}
    \new PianoStaff \with {
      instrumentName = "{{ ins.part_name() }}"
      {%- if ins.abbr %}
      shortInstrumentName = "{{ ins.abbr }}"
      {%- endif %}
      {%- if ins.midi %}
      midiInstrument = #"{{ ins.midi }}"
      {%- endif %}
    } <<
      \new Staff = "RH" {
      \new Voice  {
        <<
          {%- if loop.index == 1 %}
          {{ lyglobal.var_name(mov.num) }}
          {%- endif %}
          {{ ins.var_name(mov.num) }}_LH
        >>
      }
    }
    \new Staff = "LH" {
      \new Voice {
          {{ ins.var_name(mov.num) }}_RH
        }
      }
    >>
    {%- endif %}
    {%- endfor %}
  }
{% endfor %}
{%- endblock %}

{# vim: se ft=lilypond: #}
