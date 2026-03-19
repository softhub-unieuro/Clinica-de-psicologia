# Generated migration for ContatoUrgencia model
# This migration creates the new ContatoUrgencia table to support multiple emergency contacts

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0005_inscritocomunidade_idx_dthinsc_comun_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContatoUrgencia',
            fields=[
                ('idcontatourgencia', models.AutoField(primary_key=True, serialize=False)),
                ('nomecontato', models.CharField(help_text='Nome da pessoa de contato', max_length=50)),
                ('telefonecontato', models.CharField(help_text='Telefone para contato', max_length=15)),
                ('sequencia', models.PositiveIntegerField(default=1, help_text='Ordem do contato (1, 2 ou 3)')),
                ('idfichaconvenio', models.ForeignKey(blank=True, db_column='idfichaconvenio', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contatos_urgencia', to='formulario.inscritoconvenio')),
                ('idfichacomunidade', models.ForeignKey(blank=True, db_column='idfichacomunidade', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contatos_urgencia', to='formulario.inscritocomunidade')),
            ],
            options={
                'db_table': 'contatourgencia',
                'managed': True,
            },
        ),
        migrations.AddConstraint(
            model_name='contatourgencia',
            constraint=models.CheckConstraint(check=models.Q(('sequencia__in', [1, 2, 3])), name='sequencia_valida_1_a_3'),
        ),
        migrations.AddConstraint(
            model_name='contatourgencia',
            constraint=models.UniqueConstraint(condition=models.Q(('idfichacomunidade__isnull', False)), fields=('idfichacomunidade', 'sequencia'), name='unique_sequencia_comunidade'),
        ),
        migrations.AddConstraint(
            model_name='contatourgencia',
            constraint=models.UniqueConstraint(condition=models.Q(('idfichaconvenio__isnull', False)), fields=('idfichaconvenio', 'sequencia'), name='unique_sequencia_convenio'),
        ),
    ]
