from django.contrib import admin
from .models import Card, ProfileCard, CollectionCategory, CardRarity, Lesson


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rarity')
    list_filter = ('category', 'rarity')
    search_fields = ('name',)
    ordering = ('category', 'rarity')
    fieldsets = (
        (None, {
            'fields': ('name', 'image_name', 'category', 'rarity', 'description', 'price_to_unlock')
        }),
    )


@admin.register(ProfileCard)
class ProfileCardAdmin(admin.ModelAdmin):
    list_display = ('profile', 'card', 'unlocked_at')
    list_filter = ('unlocked_at', 'card__category', 'card__rarity')
    search_fields = ('user__username', 'card__name')
    ordering = ('-unlocked_at',)


@admin.register(CollectionCategory)
class CollectionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

@admin.register(CardRarity)
class CardRarityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    list_display = ('title', 'slug', 'chapter', 'order')