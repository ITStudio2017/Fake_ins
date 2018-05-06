from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager

from .storage import ImageStorage


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    USERS_AUTO_ACTIVATE = not settings.USERS_VERIFY_EMAIL

    email = models.EmailField(
        _('email address'), max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=USERS_AUTO_ACTIVATE,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_type = models.ForeignKey(ContentType, null=True, editable=False)

    objects = UserInheritanceManager()
    base_objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):

    """
    Concrete class of AbstractUser.
    Use this if you don't need to extend User.
    """
    GENDER_CHOICES=(
        (1,'男'),
        (2,'女'),
        (3,'保密'),
        )
    profile_picture = models.ImageField(upload_to='images',verbose_name=u"头像",storage=ImageStorage(),default="") #头像
    username = models.CharField(blank=False,unique=True,verbose_name=u"账号名",max_length=15,default="用户") #用户名，唯一
    nickname = models.CharField(max_length=15,verbose_name=u"昵称",default="") #昵称
    gender = models.IntegerField(default=3,verbose_name=u"性别",choices=GENDER_CHOICES) #性别
    address = models.CharField(blank=True,verbose_name=u"地址",max_length=30,default="")
    introduction = models.CharField(blank=True,verbose_name=u"个人简介",default="",max_length=100)
    birthday = models.DateField(verbose_name=u"生日",default="2000-01-01")
    followed_num = models.PositiveIntegerField(verbose_name=u"被关注数",default=0) #关注该用户的人的数量
    following_num = models.PositiveIntegerField(default=0,verbose_name=u"关注数") #该用户关注的人的数量




    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
