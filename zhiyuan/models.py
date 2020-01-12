from django.db import models

# Create your models here.

class SchoolOverViewItem(models.Model):
    public_private = (
        ('pub', "公立"),
        ('private', "私立")，
        ('private_pub', '公私结合'),
        ('others', '其它')
            )
    benke_zhuanke = (
        ("bk", "本科"),
        ("zk", "专科"),
        ("others", "其它")
    )
    logo = models.URLField(max_length=255, unique=True)
    name = models.CharField(primary_key=True, max_length=255, unique=True)
    address = models.CharField(max_length=255, help_text="所在地址", null=False)
    province = models.CharField(max_length=50, help_text="所在省份", null=False)
    city = models.CharField(max_length=50, help_text="所在市区", null=False,)
    is_211 = models.BooleanField(default=0)
    is_985 = models.BooleanField(default=0)
    school_types = models.CharField(max_length=255, default="")
    tags = models.CharField(max_length=255, help_text="标签列表的json字符串: 985,211")
    pub_pri = models.CharField(choices=public_private)
    bk_zk = models.CharField(choices=benke_zhuanke)
    description = models.TextField()

    class Meta:
        verbose_name = _("SchoolOverViewItem")
        verbose_name_plural = _("SchoolOverViewItems")
        unique_together = ('name', 'province', 'is_985', 'is_211', 'school_types')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SchoolOverViewItem_detail", kwargs={"pk": self.pk})
