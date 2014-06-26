# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'blog_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Category'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('is_from', self.gf('django.db.models.fields.CharField')(default='Y', max_length=1)),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'blog', ['Article'])

        # Adding M2M table for field tags on 'Article'
        m2m_table_name = db.shorten_name(u'blog_article_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'blog.article'], null=False)),
            ('tag', models.ForeignKey(orm[u'blog.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'tag_id'])

        # Adding model 'PageView'
        db.create_table(u'blog_pageview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('today', self.gf('django.db.models.fields.IntegerField')()),
            ('yesterday', self.gf('django.db.models.fields.IntegerField')()),
            ('week', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'blog', ['PageView'])

        # Adding model 'Blog'
        db.create_table(u'blog_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('page_view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.PageView'])),
        ))
        db.send_create_signal(u'blog', ['Blog'])

        # Adding model 'Comment'
        db.create_table(u'blog_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('references', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Article'])),
        ))
        db.send_create_signal(u'blog', ['Comment'])

        # Adding model 'Category'
        db.create_table(u'blog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'blog', ['Category'])

        # Adding model 'Tag'
        db.create_table(u'blog_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'blog', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table(u'blog_article')

        # Removing M2M table for field tags on 'Article'
        db.delete_table(db.shorten_name(u'blog_article_tags'))

        # Deleting model 'PageView'
        db.delete_table(u'blog_pageview')

        # Deleting model 'Blog'
        db.delete_table(u'blog_blog')

        # Deleting model 'Comment'
        db.delete_table(u'blog_comment')

        # Deleting model 'Category'
        db.delete_table(u'blog_category')

        # Deleting model 'Tag'
        db.delete_table(u'blog_tag')


    models = {
        u'blog.article': {
            'Meta': {'object_name': 'Article'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_from': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '1'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        u'blog.blog': {
            'Meta': {'object_name': 'Blog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.PageView']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'blog.comment': {
            'Meta': {'object_name': 'Comment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Article']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'references': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'blog.pageview': {
            'Meta': {'object_name': 'PageView'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'today': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'week': ('django.db.models.fields.IntegerField', [], {}),
            'yesterday': ('django.db.models.fields.IntegerField', [], {})
        },
        u'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['blog']