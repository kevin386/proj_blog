# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Comment.references'
        db.delete_column(u'blog_comment', 'references')

        # Adding field 'Comment.user_name'
        db.add_column(u'blog_comment', 'user_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32),
                      keep_default=False)

        # Adding field 'Comment.email'
        db.add_column(u'blog_comment', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True),
                      keep_default=False)

        # Adding field 'Comment.reply'
        db.add_column(u'blog_comment', 'reply',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Comment'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Comment.references'
        db.add_column(u'blog_comment', 'references',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Comment.user_name'
        db.delete_column(u'blog_comment', 'user_name')

        # Deleting field 'Comment.email'
        db.delete_column(u'blog_comment', 'email')

        # Deleting field 'Comment.reply'
        db.delete_column(u'blog_comment', 'reply_id')


    models = {
        u'blog.article': {
            'Meta': {'object_name': 'Article'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_from': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '1'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'content': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reply': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Comment']", 'null': 'True', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        u'blog.pageview': {
            'Meta': {'object_name': 'PageView'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'today': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'yesterday': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['blog']