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
{%- for mov in range(1, (movements + 1)) %}
  \score { % Movement {{ mov }}
    \new Staff {
      {%- if mov == 1 and piece.opus %}
      \header {
        opus = "{{ piece.opus }}"
      }
      {%- endif %}
      \new Voice {
        <<
          {{ lyglobal.var_name(mov) }}
          {%- if flags.compress_full_bar_rests %}
          \compressFullBarRests
          {%- endif %}
          {{ instrument.var_name(mov) }}
        >>
      }
    }
  }
{%- endfor %}
{%- endblock %}

