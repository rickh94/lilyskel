\version "{{ piece.version }}"
{%- if piece.language %}
\language "{{ piece.language }}"
{%- endif %}


{%- if not instrument.keyboard %}
{{ instrument.var_name(movement.num, slash=False) }} = \relative {
  \clef "{{ instrument.clef }}"
  {%- if movement.time %}
  \time {{ movement.time }}
  {%- endif %}
  {%- if movement.key %}
  \key {{ movement.key[0] }} \{{ movement.key[1]}}
  {%- endif %}
  {%- if instrument.name == 'global' and movement.tempo %}
  \tempo "{{ movement.tempo }}"
  {%- endif %}
}
{%- elif instrument.keyboard %}
{{ instrument.var_name(movement.num, slash=False) }}_RH = \relative {
  \clef "treble"
  {%- if movement.time %}
  \time {{ movement.time }}
  {%- endif %}
  {%- if movement.key %}
  \key {{ movement.key[0] }} \{{ movement.key[1]}}
  {%- endif %}
}

{{ instrument.var_name(movement.num, slash=False) }}_LH = \relative {
  \clef "bass"
  {%- if movement.time %}
  \time {{ movement.time }}
  {%- endif %}
  {%- if movement.key %}
  \key {{ movement.key[0] }} \{{ movement.key[1]}}
  {%- endif %}
}
{% endif %}
