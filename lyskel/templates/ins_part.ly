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
    \new Staff {
      {%- if mov.num == 1 and piece.opus %}
      \header {
        opus = "{{ piece.opus }}"
      }
      {%- endif %}
      \new Voice {
        <<
          {%- if mov.time %}
          \time {{ mov.time }}
          {%- endif %}
          {%- if mov.key %}
          \key {{ mov.key[0] }} \{{ mov.key[1]}}
          {%- endif %}
          {{ lyglobal.var_name(mov.num) }}
          {%- if flags.compress_full_bar_rests %}
          \compressFullBarRests
          {%- endif %}
          {{ instrument.var_name(mov.num) }}
        >>
      }
    }
  }
{%- endfor %}
{%- endblock %}

