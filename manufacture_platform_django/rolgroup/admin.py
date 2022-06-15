from django.contrib import admin

from django.utils.html import format_html

from .models import *

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('id', 'box_number', 'cell_number')
    list_filter = ('box_number', 'cell_number')
    search_fields = ('box_number', 'cell_number')
    list_display_links = ('box_number', 'cell_number')
    save_on_top = True
    save_as = True


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_status',)
    list_filter = ('name_status',)
    search_fields = ('name_status',)
    list_display_links = ('name_status',)
    save_on_top = True
    save_as = True


@admin.register(DIM)
class DIMAdmin(admin.ModelAdmin):
    list_display = ('id', 'dim', 'can_cut')
    list_filter = ('dim', 'can_cut')
    search_fields = ('dim', 'can_cut')
    list_display_links = ('dim', 'can_cut')
    save_on_top = True
    save_as = True


@admin.register(Classes)
class Classes(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'dim')
    list_filter = ('class_name', 'dim')
    search_fields = ('class_name',)
    list_display_links = ('class_name',)
    save_on_top = True
    save_as = True


@admin.register(Materials)
class Materials(admin.ModelAdmin):
    list_display = ('id', 'material_name', 'class_id', 'weight', 'default_lenght', 'good_cut')
    list_filter = ('material_name', 'class_id', 'weight', 'default_lenght', 'good_cut')
    search_fields = ('material_name', 'weight', 'default_lenght', 'good_cut')
    list_display_links = ('material_name', 'weight', 'default_lenght', 'good_cut')
    save_on_top = True
    save_as = True


@admin.register(Colors)
class Colors(admin.ModelAdmin):
    list_display = ('id', 'color_name', 'color_short', 'rgb', 'color_alutech')
    list_filter = ('color_name', 'color_short', 'rgb', 'color_alutech')
    search_fields = ('color_name', 'color_short', 'rgb', 'color_alutech')
    list_display_links = ('color_name', 'color_short', 'rgb', 'color_alutech')
    save_on_top = True
    save_as = True


@admin.register(Parts)
class Parts(admin.ModelAdmin):
    list_display = ('id', 'material_id', 'artnumber', 'color_id', 'price')
    raw_id_fields = ('material_id',)
    list_filter = ('material_id', 'artnumber', 'color_id', 'price')
    search_fields = ('artnumber', 'price')
    list_display_links = ('artnumber',)
    save_on_top = True
    save_as = True


@admin.register(Stock)
class Stock(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'length', 'barcode', 'shelf', 'parts')
    raw_id_fields = ('shelf', 'parts')
    list_filter = ('quantity', 'length', 'barcode')
    search_fields = ('quantity', 'length', 'barcode')
    list_display_links = ('quantity',)
    save_on_top = True
    save_as = True


@admin.register(Composition)
class Composition(admin.ModelAdmin):
    list_display = ('id', 'length', 'need_count', 'quantity', 'parts', 'rollets')
    raw_id_fields = ('parts', 'rollets')
    list_filter = ('length', 'need_count', 'quantity')
    search_fields = ('length', 'need_count', 'quantity', 'parts__id', 'rollets__id')
    list_display_links = ('length',)
    save_on_top = True
    save_as = True


@admin.register(Rollets)
class Rollets(admin.ModelAdmin):
    list_display = ('id', 'width', 'height', 'project', 'parts')
    raw_id_fields = ('project', 'parts')
    list_filter = ('width', 'height')
    search_fields = ('width', 'height')
    list_display_links = ('width',)
    save_on_top = True
    save_as = True


@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = ('id', 'receipt_date', 'status', 'deadline_date')
    list_filter = ('receipt_date', 'status', 'deadline_date')
    search_fields = ('receipt_date', 'status', 'deadline_date')
    list_display_links = ('id',)
    save_on_top = True
    save_as = True


@admin.register(Queue)
class Queue(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'length', 'parts')
    raw_id_fields = ('project', 'parts')
    list_filter = ('quantity', 'length')
    search_fields = ('quantity', 'length', 'parts__artnumber', 'parts__id')
    list_display_links = ('id', 'quantity', 'length')
    save_on_top = True
    save_as = True


@admin.register(Documents)
class Documents(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'name_dow')
    list_filter = ('name', 'file', 'name_dow')
    search_fields = ('name', 'file', 'name_dow')
    list_display_links = ('name',)
    save_on_top = True
    save_as = True