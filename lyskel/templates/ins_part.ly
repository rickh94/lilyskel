{% extends 'basepart.ly' %}
{%- block IDblock %}
% {{ filename }} - part for {{ instrument.part_name() }} of {{ piece.headers.title }}
{%- endblock %}

{% block globalheader %}
{%- if flags.key_in_partname %}
  instrument = "{{ instrument.part_name(key=True) }}"
{%- else %}
  instrument = "{{ instrument.part_name() }}"
{%- endif %}
{% endblock %}

{%- block book %}
{%- for mov in piece.movements %}
  \score { % Movement {{ mov.num }}
  {%- if not instrument.keyboard %}
    \new Staff {
      {%- if mov.num == 1 and piece.opus %}
      \header {
        opus = "{{ piece.opus }}"
      }
      {%- endif %}
      \new Voice {
        <<
          {{ lyglobal.var_name(mov.num) }}
          {%- if flags.compress_full_bar_rests %}
          \compressFullBarRests
          {%- endif %}
          {{ instrument.var_name(mov.num) }}
        >>
      }
    }
    {%- elif instrument.keyboard %}
    \new PianoStaff <<
      \new Staff = "RH" {
        <<
          {{ lyglobal.var_name(mov.num) }}
          {%- if flags.compress_full_bar_rests %}
          \compressFullBarRests
          {%- endif %}
          {{ instrument.var_name(mov.num) }}_RH
        >>
      }
      \new Staff = "LH" {
        {%- if flags.compress_full_bar_rests %}
        \compressFullBarRests
        {%- endif %}
        {{ instrument.var_name(mov.num) }}_LH
      }
    >>
    {%- endif %}
  }
{%- endfor %}
{%- endblock %}

