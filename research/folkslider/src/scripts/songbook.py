#!/usr/bin/env python3

import click
from os import listdir
from os.path import isfile, join, splitext
import pyratemp
import yaml
import mistune
import marktex

class Songbook():
    def __init__(self, settings):
        self.lyrics_tex = mistune.Markdown(renderer=marktex.LyricsRenderer(escape=False))
        with open(settings) as f:
            self.settings = yaml.load(f.read())
      
    def load(self, file_name, dir=''):
        try:
            with open(join(self.settings['root_dir'], 
                    self.settings['data_dir'], dir, file_name), 
                    encoding='utf-8') as f:
                return yaml.load(f.read())
        except Exception as e:
            print ("songbook.py: Can't open file %s -- %s. Exiting program." % 
                    (file_name, e))
            sys.exit(1)
      
    def make_book(self, output_type='tex'):
        stream = []
        book_data = []
        
        for chapter_name in self.settings['book']['chapters']:
            book_data.append({'chapter name': chapter_name, 'songs':{}})
        
        for file in listdir(join(
                self.settings['root_dir'], 
                self.settings['data_dir'],
                self.settings['songs_dir'])):
            cur_song = self.load(file, self.settings['songs_dir'])
            song_name = splitext(file)[0]
            cur_chapter = cur_song['chapter']
            for chapter in book_data: 
                if chapter['chapter name'] == cur_chapter:
                    chapter['songs'][song_name] = cur_song
                    stream.extend(self.process_song(song_name=song_name, 
                            output_type=output_type))
        stream.append(self.output(book_data, self.settings['book']['filename'],
                self.settings['templates'][output_type]['book']))
        return stream
    
    def process_song(self, song_name, output_type):
        song_data = self.load('%s.yaml' % song_name, 
            self.settings['songs_dir'])
        stream =[]
        stream.append(self.output(song_data, song_name, 
                self.settings['templates'][output_type]['leadsheet']))
        stream.append(self.output(song_data, song_name, 
                self.settings['templates'][output_type]['score']))
        return stream
    
    def output(self, data, name, template):
        
            
        template_data = self.load('%s.yaml' % template['name'], 
                self.settings['templates_dir'])
        template_args = {}
        template_args['string'] = template_data['template']
        template_args['data'] = {}
        template_args['data'][template['name']] = data
        template_args['data']['score_name'] = name
        template_args['data']['render'] = {}
        for r in template['renderers']:
            template_args['data']['render'][r] = getattr(self, 
                    r)
        template_args['escape'] = None
        file_name = '%s.%s' % (name, template_data['extension'])
        output_dir = template['directory']
        print('Rendering %s' % file_name)
        file_stream = pyratemp.Template(**template_args)()
        return (file_name, output_dir, file_stream)
        
    
    # Write
    def write_files(self, files):
        for file in files:
            path = join(file[1], file[0])
            print('Writing:\t\t%s' % path)
            with open(join(self.settings['root_dir'], path), 'w+', 
                        encoding='utf-8') as f:
                f.write(file[2])
                print('Success!')
@click.command()
@click.option('--settings-file', '-s')
def main(settings_file):
    book = Songbook(settings_file)
    book.write_files(book.make_book('tex'))
    
if __name__ == '__main__':
    main()
