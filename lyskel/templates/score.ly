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
    \new Staff { % {{ ins.part_name() }}
      \new Voice = "{{ ins.name }}" {
        <<
          {%- if loop.index == 1 %}
          {{ lyglobal.var_name(mov.num) }}
          {%- endif %}
          {{ ins.var_name(mov.num) }}
        >>
      }
    }
    {%- endfor %}
  }
{% endfor %}
{%- endblock %}
