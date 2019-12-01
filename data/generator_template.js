
// Old generator template
[
  '{{repeat(8)}}',
 {
    id:'{{index()}}',
    name:'{{firstName()}} {{surname()}}',
    username:function(){
      return 'user'+this.id;
    },
    email:function(){
      return this.username+'@gmail.com';
    },
    password:'pass',
    img:'https://via.placeholder.com/400/{{integer(700, 999)}}/fff',
    bars:[
      '{{repeat(5, 15)}}',
      {
        id:'{{index()}}',
        area:'{{random("The Mission", "Haight", "Castro", "Lower Nob-Hill")}}',
        bar_name:'{{random("Rye", "HiTops", "The Alembic", "Horsefeather", "Beaux", "Zam Zam", "Fireside Bar", "Atlas Room","Tempest","Toad Hall","Jones")}}',
        img:function(tags){
          return 'https://via.placeholder.com/400/' +
            tags.integer(700, 999) +
            '/fff/?text=' + this.name;
        },
        locations:[
          '{{repeat(5, 15)}}',
          {
            id:'{{index()}}',
            lat: '{{floating(37.799357, 37.701306)}}',
            lng: '{{floating(-122.507775, -122.377404)}}',
            img:'https://via.placeholder.com/400x300',
            icon:'icon.png'
          }
        ]
      }
    ]
 }
 ]