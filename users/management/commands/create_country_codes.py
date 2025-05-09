from django.core.management.base import BaseCommand
from users.models import CountryCode

class Command(BaseCommand):
    help = 'Creates country codes for phone numbers'

    def handle(self, *args, **kwargs):
        # Define common country codes
        country_data = [
            {"name": "India", "code": "+91", "flag_emoji": "🇮🇳"},
            {"name": "United States", "code": "+1", "flag_emoji": "🇺🇸"},
            {"name": "United Kingdom", "code": "+44", "flag_emoji": "🇬🇧"},
            {"name": "Australia", "code": "+61", "flag_emoji": "🇦🇺"},
            {"name": "Canada", "code": "+1", "flag_emoji": "🇨🇦"},
            {"name": "Singapore", "code": "+65", "flag_emoji": "🇸🇬"},
            {"name": "Malaysia", "code": "+60", "flag_emoji": "🇲🇾"},
            {"name": "China", "code": "+86", "flag_emoji": "🇨🇳"},
            {"name": "Japan", "code": "+81", "flag_emoji": "🇯🇵"},
            {"name": "South Korea", "code": "+82", "flag_emoji": "🇰🇷"},
            {"name": "Germany", "code": "+49", "flag_emoji": "🇩🇪"},
            {"name": "France", "code": "+33", "flag_emoji": "🇫🇷"},
            {"name": "Italy", "code": "+39", "flag_emoji": "🇮🇹"},
            {"name": "Spain", "code": "+34", "flag_emoji": "🇪🇸"},
            {"name": "Netherlands", "code": "+31", "flag_emoji": "🇳🇱"},
            {"name": "Russia", "code": "+7", "flag_emoji": "🇷🇺"},
            {"name": "Brazil", "code": "+55", "flag_emoji": "🇧🇷"},
            {"name": "Mexico", "code": "+52", "flag_emoji": "🇲🇽"},
            {"name": "South Africa", "code": "+27", "flag_emoji": "🇿🇦"},
            {"name": "Nigeria", "code": "+234", "flag_emoji": "🇳🇬"},
            {"name": "Egypt", "code": "+20", "flag_emoji": "🇪🇬"},
            {"name": "Saudi Arabia", "code": "+966", "flag_emoji": "🇸🇦"},
            {"name": "United Arab Emirates", "code": "+971", "flag_emoji": "🇦🇪"},
            {"name": "Turkey", "code": "+90", "flag_emoji": "🇹🇷"},
            {"name": "Israel", "code": "+972", "flag_emoji": "🇮🇱"},
            {"name": "Thailand", "code": "+66", "flag_emoji": "🇹🇭"},
            {"name": "Vietnam", "code": "+84", "flag_emoji": "🇻🇳"},
            {"name": "Indonesia", "code": "+62", "flag_emoji": "🇮🇩"},
            {"name": "Philippines", "code": "+63", "flag_emoji": "🇵🇭"},
            {"name": "New Zealand", "code": "+64", "flag_emoji": "🇳🇿"},
        ]
        
        count = 0
        for country in country_data:
            _, created = CountryCode.objects.get_or_create(
                name=country["name"],
                defaults={
                    "code": country["code"],
                    "flag_emoji": country["flag_emoji"]
                }
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Created country code for {country["name"]}'))
        
        if count == 0:
            self.stdout.write(self.style.WARNING('No new country codes created. They may already exist.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {count} country codes'))